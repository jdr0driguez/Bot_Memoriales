# main.py
import sys
import os

# Añadir el directorio actual al path para importar logger
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import setup_logger

from core.API_Consumo import consumir_api_y_procesar

# Configurar logger específico para el main
logger = setup_logger("Main")

def main():
    logger.info("Iniciando proceso principal de automatización")
    
    try:
        # Consumir API y procesar elementos (mismo flujo que test_consumo.py)
        logger.info("Consumiendo API y procesando elementos")
        resultados = consumir_api_y_procesar()
        
        # Mostrar resultados
        logger.info(f"Procesamiento completado. Total de resultados: {len(resultados)}")
        
        print("\nResultados por transacción:")
        for r in resultados:
            status = "Éxito" if r.exito else "Error"
            print(f"- {r.expediente}: {status} — {r.mensaje}")
            
            # Log del resultado individual
            if r.exito:
                logger.info(f"Transacción exitosa: {r.expediente} - {r.mensaje}")
            else:
                logger.error(f"Transacción fallida: {r.expediente} - {r.mensaje}")
        
        # Resumen final
        exitos = sum(1 for r in resultados if r.exito)
        errores = len(resultados) - exitos
        
        logger.info(f"Resumen final: {exitos} exitos, {errores} errores")
        print(f"\nResumen: {exitos} exitos, {errores} errores")
        
    except Exception as e:
        logger.error(f"Error en el proceso principal: {e}")
        print(f"Error en el proceso principal: {e}")
        return 1
    
    logger.info("Proceso principal completado exitosamente")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
