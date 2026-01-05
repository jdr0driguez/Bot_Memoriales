# archivo: API_parser.py
from typing import Any, List
import sys
import os

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from core.API_Modelos import Elemento, ApiResponse

logger = setup_logger("APIParser")


def _get_int(data: dict[str, Any], *keys: str, default: int = 0) -> int:
    """Helper: intenta leer int desde varias keys posibles."""
    for k in keys:
        v = data.get(k, None)
        if v is not None and str(v).strip() != "":
            try:
                return int(v)
            except Exception:
                pass
    return default


def parse_elemento(data: dict[str, Any]) -> Elemento:
    logger.debug(
        f"Parseando elemento: Expediente={data.get('Expediente', 'N/A')}, "
        f"ID={data.get('IdExpediente', 'N/A')}"
    )
    elemento = Elemento(
        ImportId=_get_int(data, "ImportId", "importId", default=0),
        Correlativo=_get_int(data, "Correlativo", "correlativo", default=0),

        IdExpediente=_get_int(data, "IdExpediente", "idExpediente", default=0),
        Expediente=data.get("Expediente", "") or "",
        IdTipoProceso=_get_int(data, "IdTipoProceso", "idTipoProceso", default=0),
        IdPlantilla=_get_int(data, "IdPlantilla", "idPlantilla", default=0),
        SubEtapaInicialId=_get_int(data, "SubEtapaInicialId", "subEtapaInicialId", default=0),

        CorreoRemitente=data.get("CorreoRemitente", "") or "",
        CorreoCopia=data.get("CorreoCopia", "") or "",
        # tu API manda "Contrasena" según tu código anterior
        CorreoPass=data.get("Contrasena", "") or "",
        CorreoCopiaOculta=data.get("CorreoCopiaOculta", "") or ""
    )

    logger.debug(f"Elemento parseado exitosamente: {elemento.Expediente}")
    return elemento


def parse_api_response(json_data: dict[str, Any]) -> ApiResponse:
    logger.debug("Iniciando parsing de respuesta de API")

    element_data = json_data.get("Elements")
    logger.debug(f"Datos de elementos encontrados: {type(element_data)}")

    if element_data is None:
        logger.warning("No se encontraron elementos en la respuesta de la API")
        elementos: List[Elemento] = []
    elif isinstance(element_data, list):
        logger.info(f"Parseando {len(element_data)} elementos de la lista")
        elementos = [parse_elemento(e) for e in element_data]
    else:
        logger.info("Parseando elemento único")
        elementos = [parse_elemento(element_data)]

    success = bool(json_data.get("Success", False))
    code_result = int(json_data.get("CodeResult", -1))
    message = json_data.get("Message", "") or ""

    logger.debug(f"Resultado del parsing: Success={success}, Code={code_result}, Elementos={len(elementos)}")

    return ApiResponse(
        Success=success,
        CodeResult=code_result,
        Message=message,
        Element=elementos
    )
