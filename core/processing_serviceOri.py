# processing_service.py
import logging
import datetime
from typing import Dict, Any
import sys
import os

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from core.API_Modelos import Elemento, ResultadoTransaccion
from core.db_Connection import get_db_connection
from core.repository import fetch_campos_especificos, fetch_nombre_plantilla, fetch_campos_idDemandado, fetch_correo_juzgado, fetch_plantilla_correo, fetch_idDemandado, fetch_nomDocumento, fetch_tipoPlantilla
from core.descargaPlantillaSFTP import descargar_archivo_sftp
from core.email_service import send_email_with_attachment
from config import KEYHASH
from core.dcryptCsharp import decrypt_aes_csharp
from core.estado_service import actualizar_estado_expediente

# Configurar logger específico para este módulo
logger = setup_logger("ProcessingService")

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
            if CorreoJuzgado is None:
                logger.error(f"No existe correo del juzgado con IdExpediente={e.IdExpediente}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe correo del juzgado con IdExpediente={e.IdExpediente}"
                )
            logger.debug(f"Correo del juzgado encontrado: {CorreoJuzgado}")
            
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

            # Busqueda de IdDemandado con el Documento del demandado
            logger.debug(f"Buscando IdDemandado para documento={docDemandado1}")
            resulIdDemandado = fetch_campos_idDemandado(conn, docDemandado1)
            if resulIdDemandado is None:
                logger.error(f"No existe idDemandado para documento={docDemandado1}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe idDemandado con IdExpediente={e.IdExpediente}"
                )
            
            # Desempaqueta en variables IdDemandado
            idDemandado = resulIdDemandado
            logger.debug(f"IdDemandado encontrado: {idDemandado}")

            #Validamos el tipo de plantilla para ver si va con adjunto o no
            tipoPlantilla = fetch_tipoPlantilla(conn, e.IdPlantilla, e.IdExpediente)

            # Aquí va el resto de tu lógica con esas variables...
           
            # Seteamos el nombre del documento a buscar para el anexo del correo
            fileName = fetch_nomDocumento(conn, e.IdPlantilla, e.IdExpediente)
            logger.debug(f"Nombre del archivo a descargar: {fileName}")

            # Descargamos el documento del servidor
            logger.info(f"Descargando archivo SFTP: {fileName}")
            local_path = descargar_archivo_sftp(fileName)
            if local_path is None:
                logger.error(f"No se pudo descargar el archivo: {fileName}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe documento para descargar con IdExpediente={e.IdExpediente}"
                )
            logger.info(f"Archivo descargado exitosamente: {local_path}")

            logger.info(f"Preparando envío de correo para expediente {e.Expediente}")
            cuerpoCorreo = fetch_plantilla_correo(conn, e.IdPlantilla, e.IdExpediente)

            # Validación adicional de campos obligatorios antes del envío
            if not e.CorreoPass or e.CorreoPass.strip() == "":
                logger.error(f"Campo CorreoPass está vacío para expediente {e.Expediente}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Campo CorreoPass está vacío o no existe"
                )
                
            if not e.CorreoRemitente or e.CorreoRemitente.strip() == "":
                logger.error(f"Campo CorreoRemitente está vacío para expediente {e.Expediente}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"Campo CorreoRemitente está vacío o no existe"
                )

            # Desencriptamos la contraseña
            logger.debug("Desencriptando contraseña del correo")
            passFrom = decrypt_aes_csharp(e.CorreoPass, KEYHASH)

            logger.info(f"Enviando correo para expediente {e.Expediente} a {CorreoJuzgado}")
            send_email_with_attachment(e.Expediente, 
                                       docDemandado1, 
                                       nomDemandado1, 
                                       numRadicadoLargo, 
                                       nomPlantilla, 
                                       e.CorreoRemitente, 
                                       passFrom, 
                                       CorreoJuzgado, 
                                       e.CorreoCopia, 
                                       cuerpoCorreo, 
                                       local_path)

            logger.info(f"Expediente {e.Expediente} procesado exitosamente")
            logger.debug(f"Archivo local generado: {local_path}")


            # Busqueda de IdDemandado con el idPlantilla y el idExpediente del memorial
            logger.debug(f"Buscando IdDemandado para documento={docDemandado1}")
            idDemandadoFetch = fetch_idDemandado(conn, e.IdPlantilla, e.IdExpediente)
            if idDemandadoFetch is None:
                logger.error(f"No existe idDemandado para documento={docDemandado1}")
                return ResultadoTransaccion(
                    expediente=e.Expediente,
                    exito=False,
                    mensaje=f"No existe idDemandado con IdExpediente={e.IdExpediente}"
                )
            
            
            # Actualizar estado del expediente procesado exitosamente
            logger.info(f"Actualizando estado del expediente {e.IdExpediente} con plantilla {e.IdPlantilla}")
            estado_actualizado = actualizar_estado_expediente(str(e.IdExpediente), str(e.IdPlantilla), str(idDemandadoFetch))
            
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