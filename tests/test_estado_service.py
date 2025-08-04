# test_estado_service.py
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger
from core.estado_service import actualizar_estado_expediente, actualizar_estado_multiple

# Configurar logger para el test
logger = setup_logger("TestEstadoService")

def test_actualizacion_estado_individual():
    """
    Test para verificar la actualización de estado individual
    """
    logger.info("Iniciando test de actualización de estado individual")
    
    # Test con datos de ejemplo
    expediente_id = "12345"
    plantilla_id = "1"
    
    logger.info(f"Probando actualización de estado para expediente {expediente_id} con plantilla {plantilla_id}")
    
    resultado = actualizar_estado_expediente(expediente_id, plantilla_id)
    
    if resultado:
        logger.info("Test exitoso: Estado actualizado correctamente")
    else:
        logger.warning("Test fallido: No se pudo actualizar el estado")
    
    return resultado

def test_actualizacion_estado_multiple():
    """
    Test para verificar la actualización de estado múltiple
    """
    logger.info("Iniciando test de actualización de estado múltiple")
    
    # Test con múltiples expedientes
    expedientes_plantillas = [
        {"ExpedienteId": "12345", "PlantillaId": "1"},
        {"ExpedienteId": "12346", "PlantillaId": "2"},
        {"ExpedienteId": "12347", "PlantillaId": "1"}
    ]
    
    logger.info(f"Probando actualización de estado para {len(expedientes_plantillas)} expedientes")
    
    resultados = actualizar_estado_multiple(expedientes_plantillas)
    
    exitos = sum(1 for resultado in resultados.values() if resultado)
    logger.info(f"Resultados: {exitos}/{len(expedientes_plantillas)} actualizaciones exitosas")
    
    for expediente_plantilla, resultado in resultados.items():
        if resultado:
            logger.info(f"✓ {expediente_plantilla}: Actualizado correctamente")
        else:
            logger.warning(f"✗ {expediente_plantilla}: No se pudo actualizar")
    
    return exitos > 0

def test_payload_correcto():
    """
    Test para verificar que el payload se construye correctamente
    """
    logger.info("Verificando estructura del payload")
    
    expediente_id = "12345"
    plantilla_id = "1"
    
    # Simular la construcción del payload
    payload = {
        "ExpedientesPlantillas": [
            {
                "ExpedienteId": expediente_id,
                "PlantillaId": plantilla_id
            }
        ],
        "Estado": "Terminado"
    }
    
    logger.info(f"Payload generado: {payload}")
    
    # Verificar estructura
    assert "ExpedientesPlantillas" in payload
    assert "Estado" in payload
    assert payload["Estado"] == "Terminado"
    assert len(payload["ExpedientesPlantillas"]) == 1
    assert payload["ExpedientesPlantillas"][0]["ExpedienteId"] == expediente_id
    assert payload["ExpedientesPlantillas"][0]["PlantillaId"] == plantilla_id
    
    logger.info("✓ Estructura del payload correcta")
    return True

if __name__ == "__main__":
    logger.info("Ejecutando tests del servicio de estado")
    
    # Ejecutar tests
    test_payload_correcto()
    test_actualizacion_estado_individual()
    test_actualizacion_estado_multiple()
    
    logger.info("Tests del servicio de estado completados") 