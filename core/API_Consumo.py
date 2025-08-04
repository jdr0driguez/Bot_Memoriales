# api_consumo.py
import requests
import json
from typing import List
import sys
import os

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

from core.API_parser import parse_api_response
from core.API_Modelos import ResultadoTransaccion
from core.processing_service import process_elemento
from core.estado_service import actualizar_estado_multiple

# Configurar logger específico para este módulo
logger = setup_logger("API_Consumo")

def consumir_api_y_procesar() -> List[ResultadoTransaccion]:
    logger.info("Iniciando consumo de API para plantillas pendientes")
    
    url = "https://rocketvel.ai/backend/api/Externo/bot-plantillas-pendiente"
    logger.debug(f"Realizando petición GET a: {url}")
    
    try:
        resp = requests.get(url)
        logger.debug(f"Respuesta recibida - Status: {resp.status_code}")
    except requests.RequestException as e:
        logger.error(f"Error de conexión al consumir API: {e}")
        return []
    
    resultados: List[ResultadoTransaccion] = []
    expedientes_exitosos = []  # Lista para registrar expedientes procesados exitosamente

    if not resp.ok:
        logger.error(f"HTTP {resp.status_code} - {resp.text}")
        return resultados

    '''
    PRUEBA
    '''
    
    try:
        api_resp = parse_api_response(resp.json())
        logger.debug("Respuesta de API parseada correctamente")
    except Exception as e:
        logger.error(f"Error al parsear respuesta de API: {e}")
        return resultados
    
    # Verificar si la API respondió con éxito
    if not api_resp.Success:
        logger.error(f"API respondió con error - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}, Message: {api_resp.Message}")
        logger.error(f"Detalles del error de la API - URL: {url}, Status HTTP: {resp.status_code}")
        return resultados
    else:
        logger.info(f"API respondió exitosamente - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}")

    elementos = api_resp.Element

    # ——— Aquí validamos si no hay nada para procesar ———
    if elementos is None or (isinstance(elementos, list) and len(elementos) == 0):
        logger.warning("No hay registros para procesar")
        return resultados

    # Normalizamos a lista (si viene un único objeto)
    lista = elementos if isinstance(elementos, list) else [elementos]
    logger.info(f"Procesando {len(lista)} elemento(s) de la API")

    for i, e in enumerate(lista, 1):
        logger.info(f"Procesando elemento {i}/{len(lista)} - Expediente: {e.Expediente}")
        
        # Validar campos obligatorios antes de procesar
        if not e.CorreoPass or e.CorreoPass.strip() == "":
            logger.warning(f"Omitiendo elemento {i}/{len(lista)} - Expediente: {e.Expediente} - Campo CorreoPass está vacío o no existe")
            continue
            
        if not e.CorreoRemitente or e.CorreoRemitente.strip() == "":
            logger.warning(f"Omitiendo elemento {i}/{len(lista)} - Expediente: {e.Expediente} - Campo CorreoRemitente está vacío o no existe")
            continue
        
        logger.debug(f"Campos obligatorios validados para expediente {e.Expediente} - Procesando...")
        resultado = process_elemento(e)
        resultados.append(resultado)
        
        # Registrar expedientes exitosos para actualización masiva
        if resultado.exito:
            expedientes_exitosos.append({
                "ExpedienteId": str(e.IdExpediente),
                "PlantillaId": str(e.IdPlantilla)
            })

    logger.info(f"Procesamiento completado. {len(resultados)} resultado(s) generado(s)")
    
    # Actualizar estado de expedientes exitosos de forma masiva
    if expedientes_exitosos:
        logger.info(f"Actualizando estado de {len(expedientes_exitosos)} expedientes exitosos")
        resultados_actualizacion = actualizar_estado_multiple(expedientes_exitosos)
        
        exitos_actualizacion = sum(1 for resultado in resultados_actualizacion.values() if resultado)
        logger.info(f"Estado actualizado exitosamente para {exitos_actualizacion}/{len(expedientes_exitosos)} expedientes")
    else:
        logger.info("No hay expedientes exitosos para actualizar estado")
    
    return resultados