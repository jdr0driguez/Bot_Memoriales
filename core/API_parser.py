# archivo: api_parser.py
from typing import Any, List
import sys
import os

# Aadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from core.API_Modelos import Elemento, ApiResponse

# Configurar logger especfico para este mdulo
logger = setup_logger("APIParser")

def parse_elemento(data: dict[str, Any]) -> Elemento:
    logger.debug(f" Parseando elemento: Expediente={data.get('Expediente', 'N/A')}, ID={data.get('IdExpediente', 'N/A')}")
    
    elemento = Elemento(
        IdExpediente=data.get("IdExpediente", 0),
        Expediente=data.get("Expediente", ""),
        IdTipoProceso=data.get("IdTipoProceso", 0),
        IdPlantilla=data.get("IdPlantilla", 0),
        SubEtapaInicialId=data.get("SubEtapaInicialId", 0),
        CorreoRemitente=data.get("CorreoRemitente", ""),
        CorreoCopia=data.get("CorreoCopia", ""),
        CorreoPass=data.get("Contrasena", "")
    )
    
    logger.debug(f" Elemento parseado exitosamente: {elemento.Expediente}")
    return elemento

#def hasheo_password(CorreoPass):


def parse_api_response(json_data: dict[str, Any]) -> ApiResponse:
    logger.debug(" Iniciando parsing de respuesta de API")
    
    element_data = json_data.get("Element")
    logger.debug(f" Datos de elementos encontrados: {type(element_data)}")

    # Si Element es null o no est, devolvemos lista vaca
    if element_data is None:
        logger.warning(" No se encontraron elementos en la respuesta de la API")
        elementos: List[Elemento] = []
    elif isinstance(element_data, list):
        logger.info(f" Parseando {len(element_data)} elementos de la lista")
        elementos = [parse_elemento(e) for e in element_data]
    else:
        logger.info(" Parseando elemento nico")
        elementos = [parse_elemento(element_data)]

    success = json_data.get("Success", False)
    code_result = json_data.get("CodeResult", -1)
    message = json_data.get("Message", "")
    
    logger.debug(f" Resultado del parsing: Success={success}, Code={code_result}, Elementos={len(elementos)}")
    
    return ApiResponse(
        Success=success,
        CodeResult=code_result,
        Message=message,
        Element=elementos  # ahora siempre es lista
    )
