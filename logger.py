# logger_config.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime, timedelta
import shutil

# Importar configuración de logging
try:
    from config import ENABLE_DEBUG_LOGS, MIN_LOG_LEVEL_WHEN_DEBUG_OFF, DIAS_LOGS_MANTENER, ENABLE_AUTO_CLEANUP_LOGS
except ImportError:
    # Valores por defecto si no se encuentra config.py
    ENABLE_DEBUG_LOGS = True
    MIN_LOG_LEVEL_WHEN_DEBUG_OFF = "INFO"
    DIAS_LOGS_MANTENER = 7
    ENABLE_AUTO_CLEANUP_LOGS = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_BASE_DIR = os.path.join(BASE_DIR, ".", "logs")
LOGS_BASE_DIR = os.path.abspath(LOGS_BASE_DIR)


def _get_fecha_carpeta() -> str:
    """
    Obtiene el nombre de la carpeta para la fecha actual en formato DDMMAAAA.
    
    Returns:
        str: Nombre de carpeta con formato DDMMAAAA (ej: "24092025")
    """
    return datetime.now().strftime("%d%m%Y")


def _get_log_dir_for_date(fecha: str = None) -> str:
    """
    Obtiene el directorio de logs para una fecha específica.
    
    Args:
        fecha: Fecha en formato DDMMAAAA. Si es None, usa la fecha actual.
        
    Returns:
        str: Ruta completa al directorio de logs para la fecha
    """
    if fecha is None:
        fecha = _get_fecha_carpeta()
    
    return os.path.join(LOGS_BASE_DIR, fecha)


def _ensure_log_dir_exists(log_dir: str) -> None:
    """
    Asegura que el directorio de logs existe, creándolo si es necesario.
    
    Args:
        log_dir: Ruta del directorio de logs a crear
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)


def _get_carpetas_logs_antiguas(dias_mantener: int) -> list:
    """
    Obtiene las carpetas de logs que son más antiguas que el número de días especificado.
    
    Args:
        dias_mantener: Número de días de logs a mantener
        
    Returns:
        list: Lista de rutas de carpetas a eliminar
    """
    if dias_mantener <= 0:
        return []
    
    carpetas_a_eliminar = []
    fecha_limite = datetime.now() - timedelta(days=dias_mantener)
    
    if not os.path.exists(LOGS_BASE_DIR):
        return []
    
    for item in os.listdir(LOGS_BASE_DIR):
        item_path = os.path.join(LOGS_BASE_DIR, item)
        
        # Solo procesar directorios que coincidan con el formato DDMMAAAA
        if os.path.isdir(item_path) and len(item) == 8 and item.isdigit():
            try:
                # Convertir nombre de carpeta a fecha
                fecha_carpeta = datetime.strptime(item, "%d%m%Y")
                
                # Si la fecha es anterior al límite, marcar para eliminación
                if fecha_carpeta < fecha_limite:
                    carpetas_a_eliminar.append(item_path)
                    
            except ValueError:
                # Si no se puede parsear la fecha, ignorar
                continue
    
    return carpetas_a_eliminar


def _limpiar_logs_antiguos() -> None:
    """
    Limpia automáticamente las carpetas de logs antiguos según la configuración.
    """
    if not ENABLE_AUTO_CLEANUP_LOGS or DIAS_LOGS_MANTENER <= 0:
        return
    
    carpetas_a_eliminar = _get_carpetas_logs_antiguas(DIAS_LOGS_MANTENER)
    
    for carpeta in carpetas_a_eliminar:
        try:
            shutil.rmtree(carpeta)
            carpeta_nombre = os.path.basename(carpeta)
            # Usar print en lugar de logger para evitar recursión
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] [LogCleanup] Carpeta de logs eliminada: {carpeta_nombre}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [WARNING] [LogCleanup] No se pudo eliminar carpeta {carpeta}: {e}")


# Directorio de logs para la fecha actual
LOG_DIR = _get_log_dir_for_date()
COMBINED_LOG_FILE = os.path.join(LOG_DIR, "WS_RNEC.log")

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def setup_logger(name="app"):
    # Asegurar que el directorio de logs para la fecha actual existe
    _ensure_log_dir_exists(LOG_DIR)
    
    # Limpiar logs antiguos (solo la primera vez)
    if name == "app":  # Solo para el logger principal
        _limpiar_logs_antiguos()

    logger = logging.getLogger(name)
    
    # Configurar nivel de logging basado en la configuración
    if ENABLE_DEBUG_LOGS:
        logger.setLevel(logging.DEBUG)
        effective_level = "DEBUG"
    else:
        # Usar el nivel mínimo configurado cuando DEBUG está desactivado
        level_mapping = {
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        min_level = level_mapping.get(MIN_LOG_LEVEL_WHEN_DEBUG_OFF, logging.INFO)
        logger.setLevel(min_level)
        effective_level = MIN_LOG_LEVEL_WHEN_DEBUG_OFF

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ✅ Handler combinado (todos los niveles)
        combined_handler = TimedRotatingFileHandler(
            filename=COMBINED_LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        combined_handler.setFormatter(formatter)
        logger.addHandler(combined_handler)

        # ✅ Handlers separados por nivel
        for level_name, level_value in LOG_LEVELS.items():
            file_path = os.path.join(LOG_DIR, f"{level_name.lower()}.log")
            handler = TimedRotatingFileHandler(
                filename=file_path,
                when="midnight",
                interval=1,
                backupCount=7,
                encoding='utf-8'
            )
            handler.setLevel(level_value)
            handler.setFormatter(formatter)
            handler.addFilter(LevelFilter(level_value))
            logger.addHandler(handler)

        # ✅ Consola
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
        # Log informativo sobre la configuración de logging (solo la primera vez)
        if name == "app":  # Solo para el logger principal
            fecha_actual = _get_fecha_carpeta()
            if ENABLE_DEBUG_LOGS:
                logger.info(f"Sistema de logging inicializado - Nivel: {effective_level} (DEBUG habilitado) - Carpeta: {fecha_actual}")
            else:
                logger.info(f"Sistema de logging inicializado - Nivel: {effective_level} (DEBUG deshabilitado) - Carpeta: {fecha_actual}")
            
            # Información sobre limpieza automática
            if ENABLE_AUTO_CLEANUP_LOGS and DIAS_LOGS_MANTENER > 0:
                logger.info(f"Limpieza automática habilitada - Manteniendo {DIAS_LOGS_MANTENER} días de logs")
            else:
                logger.info("Limpieza automática deshabilitada")

    return logger
