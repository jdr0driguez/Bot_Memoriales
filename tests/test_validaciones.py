# test_validaciones.py
import json
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger
from core.API_parser import parse_api_response
from core.processing_service import process_elemento

# Configurar logger para el test
logger = setup_logger("TestValidaciones")

def test_validaciones_campos_obligatorios():
    """
    Test para verificar que las validaciones de campos obligatorios funcionen correctamente
    """
    logger.info("Iniciando test de validaciones de campos obligatorios")
    
    # Caso 1: Elemento con todos los campos obligatorios
    elemento_completo = {
        "IdExpediente": 12345,
        "Expediente": "L-2024-001",
        "IdTipoProceso": 1,
        "IdPlantilla": 1,
        "SubEtapaInicialId": 1,
        "CorreoRemitente": "test@example.com",
        "CorreoCopia": "copy@example.com",
        "Contrasena": "password123"
    }
    
    # Caso 2: Elemento sin CorreoPass
    elemento_sin_password = {
        "IdExpediente": 12346,
        "Expediente": "L-2024-002",
        "IdTipoProceso": 1,
        "IdPlantilla": 1,
        "SubEtapaInicialId": 1,
        "CorreoRemitente": "test@example.com",
        "CorreoCopia": "copy@example.com",
        "Contrasena": ""  # Campo vacío
    }
    
    # Caso 3: Elemento sin CorreoRemitente
    elemento_sin_remitente = {
        "IdExpediente": 12347,
        "Expediente": "L-2024-003",
        "IdTipoProceso": 1,
        "IdPlantilla": 1,
        "SubEtapaInicialId": 1,
        "CorreoRemitente": "",  # Campo vacío
        "CorreoCopia": "copy@example.com",
        "Contrasena": "password123"
    }
    
    # Caso 4: Elemento sin ambos campos
    elemento_sin_campos = {
        "IdExpediente": 12348,
        "Expediente": "L-2024-004",
        "IdTipoProceso": 1,
        "IdPlantilla": 1,
        "SubEtapaInicialId": 1,
        "CorreoRemitente": "",  # Campo vacío
        "CorreoCopia": "copy@example.com",
        "Contrasena": ""  # Campo vacío
    }
    
    casos_test = [
        ("Elemento completo", elemento_completo),
        ("Elemento sin password", elemento_sin_password),
        ("Elemento sin remitente", elemento_sin_remitente),
        ("Elemento sin ambos campos", elemento_sin_campos)
    ]
    
    for nombre_caso, datos in casos_test:
        logger.info(f"Probando caso: {nombre_caso}")
        
        # Crear respuesta de API simulada
        api_response = {
            "Success": True,
            "CodeResult": 200,
            "Message": "OK",
            "Element": datos
        }
        
        # Parsear respuesta
        api_resp = parse_api_response(api_response)
        
        # Verificar si el elemento debe ser procesado o omitido
        elemento = api_resp.Element[0] if isinstance(api_resp.Element, list) else api_resp.Element
        
        # Validar campos obligatorios (misma lógica que en API_Consumo.py)
        if not elemento.CorreoPass or elemento.CorreoPass.strip() == "":
            logger.warning(f"CASO OMITIDO: {nombre_caso} - Campo CorreoPass está vacío")
            continue
            
        if not elemento.CorreoRemitente or elemento.CorreoRemitente.strip() == "":
            logger.warning(f"CASO OMITIDO: {nombre_caso} - Campo CorreoRemitente está vacío")
            continue
        
        logger.info(f"CASO PROCESADO: {nombre_caso} - Campos obligatorios validados")
        
        # Intentar procesar (esto fallará en el procesamiento real, pero nos permite ver la validación)
        try:
            resultado = process_elemento(elemento)
            logger.info(f"Resultado: {resultado.expediente} - {'OK' if resultado.exito else 'ERROR'}")
        except Exception as e:
            logger.error(f"Error procesando {nombre_caso}: {e}")
    
    logger.info("Test de validaciones completado")

if __name__ == "__main__":
    test_validaciones_campos_obligatorios()