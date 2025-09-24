# estado_service.py
import requests
import json
from typing import List, Dict, Any
import sys
import os

# Añadir el directorio padre al path para importar logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Configurar logger específico para este módulo
logger = setup_logger("EstadoService")

def actualizar_estado_expediente(expediente_id: str, plantilla_id: str, demandado_id: str) -> bool:
    """
    Actualiza el estado de un expediente procesado exitosamente.
    
    Args:
        expediente_id: ID del expediente procesado
        plantilla_id: ID de la plantilla utilizada
        
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    url = "https://rocketvel.ai/backend/api/Externo/expediente-estadobotplantilla"
    
    payload = {
        "ExpedientesPlantillas": [
            {
                "ExpedienteId": expediente_id,
                "PlantillaId": plantilla_id,
                "DemandadoId": demandado_id
            }
        ],
        "Estado": "Terminado"
    }
    
    logger.info(f"Actualizando estado del expediente {expediente_id} con plantilla {plantilla_id}")
    logger.debug(f"Endpoint: {url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.put(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"Estado actualizado exitosamente para expediente {expediente_id}")
            return True
        else:
            logger.error(f"Error al actualizar estado. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Error de conexión al actualizar estado del expediente {expediente_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al actualizar estado del expediente {expediente_id}: {e}")
        return False

def actualizar_estado_multiple(expedientes_plantillas: List[Dict[str, str]]) -> Dict[str, bool]:
    """
    Actualiza el estado de múltiples expedientes procesados exitosamente.
    
    Args:
        expedientes_plantillas: Lista de diccionarios con ExpedienteId y PlantillaId
        
    Returns:
        Dict[str, bool]: Diccionario con el resultado de cada actualización
    """
    url = "https://rocketvel.ai/backend/api/Externo/expediente-estadobotplantilla"
    
    payload = {
        "ExpedientesPlantillas": expedientes_plantillas,
        "Estado": "Terminado"
    }
    
    logger.info(f"Actualizando estado de {len(expedientes_plantillas)} expedientes")
    logger.debug(f"Endpoint: {url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.put(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"Estado actualizado exitosamente para {len(expedientes_plantillas)} expedientes")
            return {f"{ep['ExpedienteId']}_{ep['PlantillaId']}": True for ep in expedientes_plantillas}
        else:
            logger.error(f"Error al actualizar estado múltiple. Status: {response.status_code}, Response: {response.text}")
            return {f"{ep['ExpedienteId']}_{ep['PlantillaId']}": False for ep in expedientes_plantillas}
            
    except requests.RequestException as e:
        logger.error(f"Error de conexión al actualizar estado múltiple: {e}")
        return {f"{ep['ExpedienteId']}_{ep['PlantillaId']}": False for ep in expedientes_plantillas}
    except Exception as e:
        logger.error(f"Error inesperado al actualizar estado múltiple: {e}")
        return {f"{ep['ExpedienteId']}_{ep['PlantillaId']}": False for ep in expedientes_plantillas} 