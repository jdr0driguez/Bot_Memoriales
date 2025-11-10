# processing_service.py
import logging
import datetime
from typing import Dict, Any
import sys
import os
from pathlib import Path
import re

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

def process_elemento(e: Elemento) -> ResultadoTransaccion:
    logger.info(f"Iniciando procesamiento del expediente {e.Expediente} (ID={e.IdExpediente})")
    
    # 1) Validar tipo de proceso
    if e.IdTipoProceso != 1:
        logger.warning(f"Tipo de proceso no válido para expediente {e.Expediente} (IdTipoProceso={e.IdTipoProceso})")
        return ResultadoTransaccion(
            expediente=e.Expediente,
            exito=False,
            mensaje=f"Tipo de proceso no válido (IdTipoProceso={e.IdTipoProceso})"
        )

    logger.info(f"Procesando expediente {e.Expediente} (ID={e.IdExpediente})")

    try:
        with get_db_connection() as conn:
            logger.debug(f"Conexión a base de datos establecida para expediente {e.Expediente}")
            
            # Búsqueda por IdExpediente
            logger.debug(f"Buscando campos específicos para IdExpediente={e.IdExpediente}")
            resultado = fetch_campos_especificos(conn, e.IdExpediente)
            if resultado is None:
                logger.error(f"No existe registro con IdExpediente={e.IdExpediente}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe registro con IdExpediente={e.IdExpediente}"
                )

            # Desempaqueta en variables IdExpediente
            nomDemandado1, docDemandado1, nomDemandado2, docDemandado2, nomDemandado3, docDemandado3, nomDemandado4, docDemandado4, numRadicadoLargo = resultado
            logger.debug(f"Datos del expediente recuperados: Demandado1={nomDemandado1}, Doc={docDemandado1}")

            #Búsqueda correo del Juzgado
            logger.debug(f"Buscando correo del juzgado para IdExpediente={e.IdExpediente}")
            CorreoJuzgado = fetch_correo_juzgado(conn, e.IdExpediente)
            
            # Validación robusta del correo del juzgado
            correo_invalido = (
                CorreoJuzgado is None or 
                not str(CorreoJuzgado).strip() or 
                str(CorreoJuzgado).strip().upper() in ["NO ESPECIFICADO", "NULL", "NONE", ""] or
                not _validar_email(str(CorreoJuzgado).strip())
            )
            
            if correo_invalido:
                logger.error(f"Correo del juzgado no válido para expediente {e.Expediente} (IdExpediente={e.IdExpediente}). "
                           f"Valor encontrado: '{CorreoJuzgado}'. Se requiere un correo electrónico válido.")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Correo del juzgado no válido o no especificado para IdExpediente={e.IdExpediente}"
                )
            
            logger.debug(f"Correo del juzgado válido encontrado: {CorreoJuzgado}")
            
            # Búsqueda por IdPlantilla
            logger.debug(f"Buscando nombre de plantilla para IdPlantilla={e.IdPlantilla}")
            resultado = fetch_nombre_plantilla(conn, e.IdPlantilla)
            if resultado is None:
                logger.error(f"No existe plantilla con IdPlantilla={e.IdPlantilla}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe registro con IdExpediente={e.IdExpediente}"
                )

            # Desempaqueta en variables IdPlantilla
            nomPlantilla = resultado
            logger.debug(f"Nombre de plantilla encontrado: {nomPlantilla}")
           
            # ------------------------------------------------------------------
            # 1) Validamos y normalizamos el tipo de plantilla
            # ------------------------------------------------------------------
            raw_tipo = fetch_tipoPlantilla(conn, e.IdPlantilla, e.IdExpediente)
            logger.info(f"Tipo de plantilla (raw): {raw_tipo!r}")

            try:
                tipoPlantilla = int(str(raw_tipo).strip())
            except Exception:
                logger.error(f"No se pudo parsear tipoPlantilla desde {raw_tipo!r}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No se pudo interpretar tipo de plantilla: {raw_tipo!r}"
                )

            if tipoPlantilla not in (2, 3):
                logger.error(f"Tipo de plantilla no soportado: {tipoPlantilla}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Tipo de plantilla no soportado: {tipoPlantilla}"
                )

            logger.info(f"Tipo de plantilla (normalizado): {tipoPlantilla} → {'SIN adjunto' if tipoPlantilla == 2 else 'CON adjunto'}")

            # ------------------------------------------------------------------
            # 2) Manejo de adjunto: solo si es tipoPlantilla == 3
            # ------------------------------------------------------------------
            local_path = None  # por defecto, no hay adjunto

            if tipoPlantilla == 3:
                logger.debug("Flujo CON adjunto: se consultará y descargará el archivo.")
                fileName = fetch_nomDocumento(conn, e.IdPlantilla, e.IdExpediente)
                logger.debug(f"Resultado fetch_nomDocumento: {fileName!r}")

                if not fileName or not str(fileName).strip():
                    logger.error(f"No hay nombre de documento configurado para adjuntar (IdExpediente={e.IdExpediente})")
                    return ResultadoTransaccion(
                        expediente=e.Expediente,
                        exito=False,
                        mensaje=f"No existe documento para adjuntar con IdExpediente={e.IdExpediente}"
                    )

                fileName = str(fileName).strip()
                logger.debug(f"Nombre del archivo a descargar (normalizado): {fileName}")

                logger.info(f"Descargando archivo SFTP: {fileName}")
                local_path = descargar_archivo_sftp(fileName)
                logger.debug(f"Resultado descargar_archivo_sftp: {local_path!r}")

                if not local_path:
                    logger.error(f"No se pudo descargar el archivo: {fileName}")
                    return ResultadoTransaccion(
                        expediente=e.Expediente,
                        exito=False,
                        mensaje=f"No existe documento para descargar con IdExpediente={e.IdExpediente}"
                    )

                logger.info(f"Archivo descargado exitosamente: {local_path}")
            else:
                # tipoPlantilla == 2 → SIN adjunto, NO tocar SFTP ni fetch_nomDocumento
                logger.info("Flujo SIN adjunto (tipo 2): no se consultará nomDocumento ni se descargará archivo.")
                local_path = None

            # ------------------------------------------------------------------
            # 3) Validación de IdDemandado ANTES de enviar correo
            # ------------------------------------------------------------------
            logger.debug(f"Validando IdDemandado para documento={docDemandado1}")
            idDemandadoFetch = fetch_idDemandado(conn, e.IdPlantilla, e.IdExpediente)
            if idDemandadoFetch is None:
                logger.error(f"No existe idDemandado para documento={docDemandado1}")
                # Limpiar archivo si se descargó antes de la validación
                if local_path:
                    _limpiar_archivo_local(local_path)
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe idDemandado con IdExpediente={e.IdExpediente}"
                )
            logger.info(f"IdDemandado validado exitosamente: {idDemandadoFetch}")

            # ------------------------------------------------------------------
            # 4) Preparación del correo
            # ------------------------------------------------------------------
            logger.info(f"Preparando envío de correo para expediente {e.Expediente}")
            cuerpoCorreo = fetch_plantilla_correo(conn, e.IdPlantilla, e.IdExpediente)

            # Validación de campos obligatorios
            if not e.CorreoPass or not e.CorreoPass.strip():
                logger.error(f"Campo CorreoPass está vacío para expediente {e.Expediente}")
                # Limpiar archivo si se descargó antes de la validación
                if local_path:
                    _limpiar_archivo_local(local_path)
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Campo CorreoPass está vacío o no existe"
                )

            if not e.CorreoRemitente or not e.CorreoRemitente.strip():
                logger.error(f"Campo CorreoRemitente está vacío para expediente {e.Expediente}")
                # Limpiar archivo si se descargó antes de la validación
                if local_path:
                    _limpiar_archivo_local(local_path)
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Campo CorreoRemitente está vacío o no existe"
                )

            # Desencriptamos la contraseña
            logger.debug("Desencriptando contraseña del correo")
            passFrom = decrypt_aes_csharp(e.CorreoPass, KEYHASH)

            # Envío del correo (si local_path es None, la función lo enviará sin adjunto)
            logger.info(f"Enviando correo para expediente {e.Expediente} a {CorreoJuzgado} (Adjunto={'Sí' if local_path else 'No'})")
            
            correo_enviado_exitosamente = False
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
                correo_enviado_exitosamente = True
                logger.info(f"Correo enviado exitosamente para expediente {e.Expediente}")
                
            except Exception as email_error:
                logger.error(f"Error al enviar correo para expediente {e.Expediente}: {email_error}")
                # Limpiar archivo incluso si falló el envío
                if local_path:
                    _limpiar_archivo_local(local_path)
                raise email_error
            
            # Limpiar archivo después del envío exitoso
            if local_path:
                logger.debug(f"Archivo local utilizado: {local_path}")
                _limpiar_archivo_local(local_path)

            logger.info(f"Expediente {e.Expediente} procesado exitosamente")

            # ------------------------------------------------------------------
            # 5) Actualizar estado del expediente
            # ------------------------------------------------------------------
            logger.info(f"Actualizando estado del expediente {e.IdExpediente} con plantilla {e.IdPlantilla}")
            estado_actualizado = actualizar_estado_expediente(
                str(e.IdExpediente),
                str(e.IdPlantilla),
                str(idDemandadoFetch)
            )

            if estado_actualizado:
                logger.info(f"Estado actualizado exitosamente para expediente {e.Expediente}")
            else:
                logger.warning(f"No se pudo actualizar el estado para expediente {e.Expediente}")

            
        return ResultadoTransaccion(
            expediente=e.Expediente,
            exito=True,
            mensaje="Procesado y lógica adicional OK"
        )

    except Exception as exc:
        logger.error(f"Error inesperado procesando expediente {e.Expediente}: {exc}")
        
        # Limpiar archivo en caso de error inesperado
        # Intentamos obtener local_path del contexto si existe
        try:
            if 'local_path' in locals() and local_path:
                _limpiar_archivo_local(local_path)
        except Exception as cleanup_error:
            logger.warning(f"Error adicional al limpiar archivo durante manejo de excepción: {cleanup_error}")
        
        return ResultadoTransaccion(
            expediente=e.Expediente,
            exito=False,
            mensaje=f"Error inesperado: {exc}"
        )

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