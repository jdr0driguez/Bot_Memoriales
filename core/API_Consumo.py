# api_consumo.py
import requests
from typing import List, Dict, Any, Optional
import sys
import os
import time

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import setup_logger
from core.API_parser import parse_api_response
from core.API_Modelos import ResultadoTransaccion
from core.processing_service import process_elemento
from core.estado_service import actualizar_estado_multiple

# ✅ Importa tus estados centralizados
from core.estados import EstadoStagingExpedienteMemoriales as E

logger = setup_logger("API_Consumo")


# ============================================================
# 1) CONFIG
# ============================================================

#BASE_URL = "http://localhost:5000"
BASE_URL = "https://rocketvel.ai/backend"

ENDPOINT_PENDIENTES = f"{BASE_URL}/api/Externo/bot-plantillas-pendiente" # Endpoint para obtener plantillas pendientes
ENDPOINT_CANCELADO = f"{BASE_URL}/api/Externo/importacion-cancelada" # Endpoint para verificar si una importación ha sido cancelada
ENDPOINT_STAGING_ESTADO = f"{BASE_URL}/api/Externo/staging-expedientes-estado" # Endpoint para actualizar el estado en staging

HTTP_TIMEOUT_GET = 30
HTTP_TIMEOUT_PUT = 20


# ============================================================
# 2) HELPERS: cancelación + actualización de staging
# ============================================================

_cancel_cache: Dict[int, Dict[str, Any]] = {}  # { importId: { "ts": float, "cancelado": bool } }


def fmt_p2_err(correlativo: int, detalle: str) -> str:
    return f"ITEM SEQ {correlativo}: {detalle}" #Error normalizado

def importacion_cancelada(import_id: int, ttl_seconds: int = 2) -> bool:
    """Consulta al backend si el import está cancelado. Cache TTL para no spamear."""
    now = time.time()
    cached = _cancel_cache.get(import_id)
    if cached and (now - cached["ts"]) < ttl_seconds:
        return bool(cached["cancelado"])

    try:
        r = requests.get(ENDPOINT_CANCELADO, params={"importId": import_id}, timeout=HTTP_TIMEOUT_GET)
        r.raise_for_status()
        data = r.json()
        cancelado = bool(data.get("Element", False))
    except Exception as ex:
        logger.warning(f"No se pudo verificar cancelación (ImportId={import_id}): {ex}")
        cancelado = False

    _cancel_cache[import_id] = {"ts": now, "cancelado": cancelado}
    return cancelado


def staging_actualizar_estado(import_id: int, correlativo: int, estado: E, mensaje_error: Optional[str] = None) -> bool:
    """
    Actualiza Staging_Expedientes por (ImportId, Correlativo).
    - Valida ServiceResponse<bool>: Success + Element.
    """
    payload = {
        "ImportId": import_id,
        "Correlativo": correlativo,
        "Estado": int(estado),        # IntEnum -> int
        "MensajeError": mensaje_error
    }

    try:
        r = requests.put(ENDPOINT_STAGING_ESTADO, json=payload, timeout=HTTP_TIMEOUT_PUT)

        # Validar respuesta tipo ServiceResponse<bool>
        try:
            data = r.json()
        except Exception:
            logger.error(
                f"Respuesta no es JSON al actualizar staging (ImportId={import_id}, Corr={correlativo}). "
                f"Status={r.status_code} Body={r.text[:200]}"
            )
            return False

        success = bool(data.get("Success", False))
        element = bool(data.get("Element", False))

        if not success or not element:
            msg = data.get("Message", "")
            logger.error(
                f"ServiceResponse indicó fallo al actualizar staging "
                f"(ImportId={import_id}, Corr={correlativo}, Estado={int(estado)}). "
                f"Success={success}, Element={element}, Message={msg}"
            )
            return False

        return True

    except requests.RequestException as ex:
        logger.error(
            f"Fallo HTTP al actualizar staging (ImportId={import_id}, Correlativo={correlativo}, Estado={int(estado)}). "
            f"Error: {ex}"
        )
        return False
    except Exception as ex:
        logger.error(
            f"Error inesperado al actualizar staging (ImportId={import_id}, Correlativo={correlativo}, Estado={int(estado)}). "
            f"Error: {ex}"
        )
        return False

# ============================================================
# 3) Flujo principal
# ============================================================

def consumir_api_y_procesar(expediente_id: int | None = None, plantilla_id: int | None = None) -> List[ResultadoTransaccion]:
    logger.info("Iniciando consumo de API para plantillas pendientes")
    logger.debug(f"Realizando petición GET a: {ENDPOINT_PENDIENTES}")

    params = {}
    if expediente_id is not None:
        params["expedienteId"] = expediente_id
    if plantilla_id is not None:
        params["plantillaId"] = plantilla_id

    try:
        resp = requests.get(ENDPOINT_PENDIENTES, params=params, timeout=HTTP_TIMEOUT_GET)
        logger.debug(f"Respuesta recibida - Status: {resp.status_code}")
        print(resp.json())
    except requests.RequestException as e:
        logger.error(f"Error de conexión al consumir API: {e}")
        return []
    
    resultados: List[ResultadoTransaccion] = []
    expedientes_exitosos = []  # para la actualización masiva existente

    if not resp.ok:
        logger.error(f"HTTP {resp.status_code} - {resp.text}")
        return resultados

    try:
        api_resp = parse_api_response(resp.json())
        logger.debug("Respuesta de API parseada correctamente")
    except Exception as e:
        logger.error(f"Error al parsear respuesta de API: {e}")
        return resultados

    if not api_resp.Success:
        logger.error(
            f"API respondió con error - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}, Message: {api_resp.Message}"
        )
        return resultados

    elementos = api_resp.Element

    if elementos is None or (isinstance(elementos, list) and len(elementos) == 0):
        logger.warning("No hay registros para procesar")
        return resultados

    lista = elementos if isinstance(elementos, list) else [elementos]
    logger.info(f"Procesando {len(lista)} elemento(s) de la API")

    for i, e in enumerate(lista, 1):
        try:
            import_id = int(getattr(e, "ImportId"))
            correlativo = int(getattr(e, "Correlativo"))
        except Exception:
            logger.error("El elemento NO trae ImportId/Correlativo")
            continue

        logger.info(f"Procesando {i}/{len(lista)} - Expediente: {e.Expediente} (ImportId={import_id}, Corr={correlativo})")

        # 1) Cancelación rápida 
        if importacion_cancelada(import_id):
            logger.warning(f"Omitiendo {i}/{len(lista)} - Expediente {e.Expediente} - Importación cancelada")
            continue

        # 2) Marcar que el bot ya tomó este registro
        staging_actualizar_estado(import_id, correlativo, E.PROCESANDO_BOT, None)

        # 3) Validaciones obligatorias
        correo_pass = (getattr(e, "CorreoPass", None) or "").strip()
        correo_remitente = (getattr(e, "CorreoRemitente", None) or "").strip()

        if not correo_pass:
            msg = "CorreoPass está vacío o no existe"
            logger.error(f"Omitiendo {i}/{len(lista)} - Expediente {e.Expediente} - {msg}")
            staging_actualizar_estado(import_id, correlativo, E.ERROR, fmt_p2_err(correlativo, msg))
            continue

        if not correo_remitente:
            msg = "CorreoRemitente está vacío o no existe"
            logger.error(f"Omitiendo {i}/{len(lista)} - Expediente {e.Expediente} - {msg}")
            staging_actualizar_estado(import_id, correlativo, E.ERROR, fmt_p2_err(correlativo, msg))
            continue

        # 4) Procesamiento principal (y manejo de errores)
        try:
            # Cancelación justo antes de operaciones pesadas
            if importacion_cancelada(import_id):
                logger.warning(f"Omitiendo {i}/{len(lista)} - Expediente {e.Expediente} - Importación cancelada antes de procesar")
                continue

            resultado = process_elemento(e, cancel_checker=importacion_cancelada)
            resultados.append(resultado)

            if resultado.exito:
                # Marcar en staging Finalizado P2
                staging_actualizar_estado(import_id, correlativo, E.FINALIZADO_P2, None)

                expedientes_exitosos.append({
                    "ExpedienteId": str(e.IdExpediente),
                    "PlantillaId": str(e.IdPlantilla)
                })
            else:
                msg = getattr(resultado, "mensaje", None) or "Error en procesamiento P2"
                if msg == "Cancelado por el usuario": #Si fue cancelado, no marcar error, solo omitir. Desde el backend, se eliminará el expediente en staging.
                    logger.info(f"Omitiendo actualización de estado en staging Expedientes para {e.Expediente} - Cancelado por el usuario") 
                    continue
                staging_actualizar_estado(import_id, correlativo, E.ERROR, fmt_p2_err(correlativo, msg))

        except Exception as ex:
            resultados.append(ResultadoTransaccion(expediente=e.Expediente, exito=False, mensaje=str(ex)))
            staging_actualizar_estado(import_id, correlativo, E.ERROR, fmt_p2_err(correlativo, f"Error inesperado: {str(ex)}"))


    logger.info(f"Procesamiento completado. {len(resultados)} resultado(s) generado(s)")

    # 5) actualización masiva actual
    if expedientes_exitosos:
        logger.info(f"Actualizando estado de {len(expedientes_exitosos)} expedientes exitosos (flujo actual)")
        resultados_actualizacion = actualizar_estado_multiple(expedientes_exitosos)

        exitos_actualizacion = sum(1 for ok in resultados_actualizacion.values() if ok)
        logger.info(f"Estado actualizado exitosamente para {exitos_actualizacion}/{len(expedientes_exitosos)} expedientes")
    else:
        logger.info("No hay expedientes exitosos para actualizar estado")

    return resultados
