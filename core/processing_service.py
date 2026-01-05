# processing_service.py
import logging
import datetime
from typing import Dict, Any
import sys
import os
from pathlib import Path
import re
from typing import Callable, Optional

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from core.API_Modelos import Elemento, ResultadoTransaccion
from core.db_Connection import get_db_connection
from core.repository import fetch_campos_especificos, fetch_nombre_plantilla, fetch_correo_juzgado, fetch_plantilla_correo, fetch_idDemandado, fetch_nomDocumento, fetch_tipoPlantilla
from core.descargaPlantillaSFTP import descargar_archivo_sftp
from core.email_service import send_email_with_attachment
from config import KEYHASH
from core.dcryptCsharp import decrypt_aes_csharp
from core.estado_service import actualizar_estado_expediente
from core.API_Consumo import importacion_cancelada;
# Configurar logger específico para este módulo
logger = setup_logger("ProcessingService")


def _limpiar_archivo_local(archivo_path: str) -> None:
    """
    Elimina de forma segura un archivo local descargado.
    
    Args:
        archivo_path: Ruta del archivo a eliminar
    """
    if not archivo_path:
        return
        
    try:
        archivo = Path(archivo_path)
        if archivo.exists() and archivo.is_file():
            archivo.unlink()
            logger.info(f"Archivo local eliminado exitosamente: {archivo_path}")
        else:
            logger.debug(f"El archivo no existe o no es un archivo válido: {archivo_path}")
    except Exception as e:
        logger.warning(f"No se pudo eliminar el archivo local {archivo_path}: {e}")
        # No lanzamos excepción para no interrumpir el flujo principal


def _validar_email(email: str) -> bool:
    """
    Valida si un string tiene formato de email válido.
    
    Args:
        email: String a validar
        
    Returns:
        bool: True si es un email válido, False en caso contrario
    """
    if not email or not isinstance(email, str):
        return False
    
    # Patrón básico para validar email
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron_email, email.strip()))

def _safe_msg(msg: str, max_len: int = 1800) -> str:
    msg = (msg or "").strip()
    return msg if len(msg) <= max_len else (msg[:max_len] + "…")


def process_elemento(e: Elemento, cancel_checker: Optional[Callable[[int], bool]] = None) -> ResultadoTransaccion:
    logger.info(f"Iniciando procesamiento del expediente {e.Expediente} (ID={e.IdExpediente})")


    # Cancelación rápida al inicio
    if importacion_cancelada(e.ImportId):
        return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="Cancelado por el usuario")

    # Validaciones tempranas (mensajes “limpios”, sin ITEM SEQ)
    if not e.CorreoPass or not str(e.CorreoPass).strip():
        return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="CorreoPass está vacío o no existe")

    if not e.CorreoRemitente or not str(e.CorreoRemitente).strip():
        return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="CorreoRemitente está vacío o no existe")

    # Validar tipo de proceso
    if e.IdTipoProceso != 1:
        return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"Tipo de proceso no válido (IdTipoProceso={e.IdTipoProceso})")

    local_path = None

    try:
        with get_db_connection() as conn:
            if importacion_cancelada(e.ImportId):
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="Cancelado por el usuario")

            # BD: campos
            try:
                resultado = fetch_campos_especificos(conn, e.IdExpediente)
            except Exception as ex:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"Error consultando campos del expediente: {ex}"))

            if resultado is None:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No existe registro con IdExpediente={e.IdExpediente}")

            nomDemandado1, docDemandado1, *_resto, numRadicadoLargo = resultado

            # BD: correo juzgado
            try:
                CorreoJuzgado = fetch_correo_juzgado(conn, e.IdExpediente)
            except Exception as ex:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"Error obteniendo correo del juzgado: {ex}"))

            correo_invalido = (
                CorreoJuzgado is None or
                not str(CorreoJuzgado).strip() or
                str(CorreoJuzgado).strip().upper() in ["NO ESPECIFICADO", "NULL", "NONE", ""] or
                not _validar_email(str(CorreoJuzgado).strip())
            )
            if correo_invalido:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"Correo del juzgado no válido o no especificado para IdExpediente={e.IdExpediente}")

            # BD: plantilla
            nomPlantilla = fetch_nombre_plantilla(conn, e.IdPlantilla)
            if nomPlantilla is None:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No existe plantilla con IdPlantilla={e.IdPlantilla}")

            raw_tipo = fetch_tipoPlantilla(conn, e.IdPlantilla, e.IdExpediente)
            try:
                tipoPlantilla = int(str(raw_tipo).strip())
            except Exception:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No se pudo interpretar tipo de plantilla: {raw_tipo!r}")

            if tipoPlantilla not in (2, 3):
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"Tipo de plantilla no soportado: {tipoPlantilla}")

            if importacion_cancelada(e.ImportId):
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="Cancelado por el usuario")

            # SFTP si adjunto
            if tipoPlantilla == 3:
                fileName = fetch_nomDocumento(conn, e.IdPlantilla, e.IdExpediente)
                if not fileName or not str(fileName).strip():
                    return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No existe documento para adjuntar con IdExpediente={e.IdExpediente}")

                if importacion_cancelada(e.ImportId):
                    return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="Cancelado por el usuario")

                try:
                    local_path = descargar_archivo_sftp(str(fileName).strip())
                except Exception as ex:
                    return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"Error descargando adjunto por SFTP: {ex}"))

                if not local_path:
                    return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No se pudo descargar el archivo para IdExpediente={e.IdExpediente}")

            # Demandado
            idDemandadoFetch = fetch_idDemandado(conn, e.IdPlantilla, e.IdExpediente)
            if idDemandadoFetch is None:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=f"No existe idDemandado con IdExpediente={e.IdExpediente}")

            cuerpoCorreo = fetch_plantilla_correo(conn, e.IdPlantilla, e.IdExpediente)

            # Decrypt
            try:
                passFrom = decrypt_aes_csharp(e.CorreoPass, KEYHASH)
            except Exception as ex:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"No se pudo desencriptar CorreoPass: {ex}"))

            if importacion_cancelada(e.ImportId):
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="Cancelado por el usuario")

            # Envío correo
            try:
                send_email_with_attachment(
                    e.Expediente,
                    docDemandado1,
                    nomDemandado1,
                    numRadicadoLargo,
                    nomPlantilla,
                    e.CorreoRemitente,
                    passFrom,
                    CorreoJuzgado,
                    e.CorreoCopia,
                    cuerpoCorreo,
                    local_path,
                    e.CorreoCopiaOculta
                )
            except Exception as ex:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"Error enviando correo: {ex}"))

            # si esto falla, NO devuelvas éxito
            ok_estado = actualizar_estado_expediente(str(e.IdExpediente), str(e.IdPlantilla), str(idDemandadoFetch))
            if not ok_estado:
                return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje="No se pudo actualizar estadoBotPlantillas en el backend")

        return ResultadoTransaccion(expediente=e.Expediente, exito=True, mensaje="OK")

    except Exception as exc:
        logger.error(f"Error inesperado procesando expediente {e.Expediente}: {exc}")
        return ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=_safe_msg(f"Error inesperado: {exc}"))

    finally:
        if local_path:
            _limpiar_archivo_local(local_path)


def _realizar_logica_adicional(
    e: Elemento,
    valor_x: int,
    valor_y: str,
    valor_z: float
) -> None:
    """
    Implementa aquí tu procesamiento extra:
      - validaciones
      - cálculos
      - llamadas a otros servicios
      - updates posteriores si lo necesitas
    """
    # ejemplo dummy:
    if valor_x < 0:
        raise ValueError("valor_x no puede ser negativo")
    # ... resto de tu lógica ...
    pass