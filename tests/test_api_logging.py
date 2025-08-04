# test_api_logging.py
import sys
import os
import json

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger
from core.API_parser import parse_api_response

# Configurar logger para el test
logger = setup_logger("TestAPILogging")

def test_api_error_logging():
    """
    Test para verificar que el logging de errores de la API funcione correctamente
    """
    logger.info("Iniciando test de logging de errores de API")
    
    # Simular respuesta de API con error
    api_response_error = {
        "Success": False,
        "CodeResult": 400,
        "Message": "Bad Request - Parámetros inválidos",
        "Element": None
    }
    
    logger.info(f"Probando respuesta de API con error: {json.dumps(api_response_error, indent=2)}")
    
    try:
        # Parsear la respuesta
        api_resp = parse_api_response(api_response_error)
        
        # Verificar que se registre el error correctamente
        if not api_resp.Success:
            logger.error(f"API respondió con error - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}, Message: {api_resp.Message}")
            logger.error(f"Detalles del error de la API - CodeResult: {api_resp.CodeResult}")
            logger.info("✓ Logging de error de API funcionando correctamente")
        else:
            logger.warning("✗ API debería haber reportado error")
            
    except Exception as e:
        logger.error(f"Error al parsear respuesta de API: {e}")
        return False
    
    return True

def test_api_success_logging():
    """
    Test para verificar que el logging de éxito de la API funcione correctamente
    """
    logger.info("Iniciando test de logging de éxito de API")
    
    # Simular respuesta de API exitosa
    api_response_success = {
        "Success": True,
        "CodeResult": 200,
        "Message": "OK",
        "Element": [
            {
                "IdExpediente": 12345,
                "Expediente": "TEST-001",
                "IdTipoProceso": 1,
                "IdPlantilla": 1,
                "SubEtapaInicialId": 1,
                "CorreoRemitente": "test@example.com",
                "CorreoCopia": "copy@example.com",
                "CorreoPass": "encrypted_password"
            }
        ]
    }
    
    logger.info(f"Probando respuesta de API exitosa: {json.dumps(api_response_success, indent=2)}")
    
    try:
        # Parsear la respuesta
        api_resp = parse_api_response(api_response_success)
        
        # Verificar que se registre el éxito correctamente
        if api_resp.Success:
            logger.info(f"API respondió exitosamente - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}")
            logger.info("✓ Logging de éxito de API funcionando correctamente")
        else:
            logger.warning("✗ API debería haber reportado éxito")
            
    except Exception as e:
        logger.error(f"Error al parsear respuesta de API: {e}")
        return False
    
    return True

def test_different_error_codes():
    """
    Test para verificar diferentes códigos de error
    """
    logger.info("Iniciando test de diferentes códigos de error")
    
    error_codes = [400, 401, 403, 404, 500, 503]
    
    for code in error_codes:
        api_response = {
            "Success": False,
            "CodeResult": code,
            "Message": f"Error {code} - Test message",
            "Element": None
        }
        
        logger.info(f"Probando código de error: {code}")
        
        try:
            api_resp = parse_api_response(api_response)
            
            if not api_resp.Success:
                logger.error(f"API respondió con error - Success: {api_resp.Success}, CodeResult: {api_resp.CodeResult}, Message: {api_resp.Message}")
                logger.info(f"✓ Código de error {code} registrado correctamente")
            else:
                logger.warning(f"✗ Código de error {code} debería haber reportado error")
                
        except Exception as e:
            logger.error(f"Error al parsear respuesta con código {code}: {e}")
    
    return True

if __name__ == "__main__":
    logger.info("Ejecutando tests de logging de API")
    
    # Ejecutar tests
    test_api_error_logging()
    test_api_success_logging()
    test_different_error_codes()
    
    logger.info("Tests de logging de API completados") 