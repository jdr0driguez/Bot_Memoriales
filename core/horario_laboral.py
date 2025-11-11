# horario_laboral.py
"""
Módulo para validar horarios laborales y días hábiles en Colombia.
Incluye manejo de festivos colombianos y zona horaria local.
"""

import sys
import os
from datetime import datetime, date, timedelta
from typing import List, Tuple
import pytz

# Añadir el directorio padre al path para importar logger y config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger

# Importar configuración
try:
    from config import (
        ENABLE_HORARIO_LABORAL, 
        HORA_INICIO_LABORAL, 
        HORA_FIN_LABORAL,
        DIAS_HABILES,
        TIMEZONE_COLOMBIA,
        ENABLE_VALIDACION_FESTIVOS
    )
except ImportError:
    # Valores por defecto
    ENABLE_HORARIO_LABORAL = True
    HORA_INICIO_LABORAL = 8
    HORA_FIN_LABORAL = 17
    DIAS_HABILES = [0, 1, 2, 3, 4]  # Lunes a Viernes
    TIMEZONE_COLOMBIA = "America/Bogota"
    ENABLE_VALIDACION_FESTIVOS = True

# Configurar logger específico para este módulo
logger = setup_logger("HorarioLaboral")


def _get_festivos_colombia(año: int) -> List[date]:
    """
    Obtiene los festivos fijos y calculados de Colombia para un año específico.
    
    Args:
        año: Año para calcular los festivos
        
    Returns:
        List[date]: Lista de fechas de festivos colombianos
    """
    festivos = []
    
    # Festivos fijos
    festivos_fijos = [
        (1, 1),   # Año Nuevo
        (5, 1),   # Día del Trabajo
        (7, 20),  # Día de la Independencia
        (8, 7),   # Batalla de Boyacá
        (12, 8),  # Inmaculada Concepción
        (12, 25), # Navidad
    ]
    
    for mes, dia in festivos_fijos:
        festivos.append(date(año, mes, dia))
    
    # Festivos que se trasladan al lunes siguiente según Ley Emiliani
    # Estos festivos SOLO son festivos si caen en lunes, si no, se trasladan al lunes siguiente
    festivos_trasladables = [
        (1, 6),   # Reyes Magos
        (3, 19),  # San José
        (6, 29),  # San Pedro y San Pablo
        (8, 15),  # Asunción de la Virgen
        (10, 12), # Día de la Raza
        (11, 1),  # Todos los Santos
        (11, 11), # Independencia de Cartagena
    ]
    
    for mes, dia in festivos_trasladables:
        fecha = date(año, mes, dia)
        # Si NO es lunes, trasladar al lunes siguiente
        if fecha.weekday() != 0:  # 0 = lunes
            dias_hasta_lunes = (7 - fecha.weekday()) % 7
            if dias_hasta_lunes == 0:  # Si es domingo
                dias_hasta_lunes = 1
            # Calcular el lunes siguiente usando timedelta para evitar problemas de días del mes
            fecha = fecha + timedelta(days=dias_hasta_lunes)
        festivos.append(fecha)
    
    # Festivos basados en Pascua (cálculo simplificado)
    # Para una implementación completa, se necesitaría una librería como dateutil
    # Por ahora, agregamos fechas aproximadas para 2025
    if año == 2025:
        festivos.extend([
            date(2025, 4, 17),  # Jueves Santo (aproximado)
            date(2025, 4, 18),  # Viernes Santo (aproximado)
            date(2025, 6, 2),   # Ascensión (aproximado)
            date(2025, 6, 23),  # Corpus Christi (aproximado)
            date(2025, 7, 7),   # Sagrado Corazón (aproximado)
        ])
    
    return sorted(festivos)


def _get_datetime_colombia() -> datetime:
    """
    Obtiene la fecha y hora actual en la zona horaria de Colombia.
    
    Returns:
        datetime: Fecha y hora actual en Colombia
    """
    try:
        tz_colombia = pytz.timezone(TIMEZONE_COLOMBIA)
        return datetime.now(tz_colombia)
    except Exception as e:
        logger.warning(f"Error al obtener zona horaria de Colombia: {e}. Usando hora local.")
        return datetime.now()


def es_dia_habil(fecha: datetime = None) -> bool:
    """
    Verifica si una fecha es día hábil en Colombia.
    
    Args:
        fecha: Fecha a verificar. Si es None, usa la fecha actual de Colombia.
        
    Returns:
        bool: True si es día hábil, False en caso contrario
    """
    if fecha is None:
        fecha = _get_datetime_colombia()
    
    # Verificar si es fin de semana
    if fecha.weekday() not in DIAS_HABILES:
        logger.debug(f"No es día hábil: {fecha.strftime('%A %d/%m/%Y')} (fin de semana)")
        return False
    
    # Verificar si es festivo (si está habilitado)
    if ENABLE_VALIDACION_FESTIVOS:
        festivos = _get_festivos_colombia(fecha.year)
        fecha_solo = fecha.date()
        
        if fecha_solo in festivos:
            logger.debug(f"No es día hábil: {fecha.strftime('%d/%m/%Y')} (festivo)")
            return False
    
    logger.debug(f"Es día hábil: {fecha.strftime('%A %d/%m/%Y')}")
    return True


def es_horario_laboral(fecha: datetime = None) -> bool:
    """
    Verifica si una fecha/hora está dentro del horario laboral.
    
    Args:
        fecha: Fecha y hora a verificar. Si es None, usa la hora actual de Colombia.
        
    Returns:
        bool: True si está en horario laboral, False en caso contrario
    """
    if fecha is None:
        fecha = _get_datetime_colombia()
    
    hora_actual = fecha.hour
    
    if HORA_INICIO_LABORAL <= hora_actual < HORA_FIN_LABORAL:
        logger.debug(f"Está en horario laboral: {fecha.strftime('%H:%M')} "
                    f"(rango: {HORA_INICIO_LABORAL}:00-{HORA_FIN_LABORAL}:00)")
        return True
    else:
        logger.debug(f"No está en horario laboral: {fecha.strftime('%H:%M')} "
                    f"(rango: {HORA_INICIO_LABORAL}:00-{HORA_FIN_LABORAL}:00)")
        return False


def debe_ejecutar_bot() -> Tuple[bool, str]:
    """
    Determina si el bot debe ejecutarse basado en horario laboral y días hábiles.
    
    Returns:
        Tuple[bool, str]: (debe_ejecutar, razon)
    """
    if not ENABLE_HORARIO_LABORAL:
        return True, "Validación de horario laboral deshabilitada"
    
    fecha_actual = _get_datetime_colombia()
    
    # Verificar día hábil
    if not es_dia_habil(fecha_actual):
        return False, f"No es día hábil: {fecha_actual.strftime('%A %d/%m/%Y')}"
    
    # Verificar horario laboral
    if not es_horario_laboral(fecha_actual):
        return False, f"Fuera de horario laboral: {fecha_actual.strftime('%H:%M')} (horario: {HORA_INICIO_LABORAL}:00-{HORA_FIN_LABORAL}:00)"
    
    return True, f"Horario laboral válido: {fecha_actual.strftime('%A %d/%m/%Y %H:%M')}"


def get_proximo_horario_laboral() -> datetime:
    """
    Calcula cuándo será el próximo horario laboral válido.
    
    Returns:
        datetime: Fecha y hora del próximo horario laboral
    """
    fecha_actual = _get_datetime_colombia()
    
    # Si estamos en día hábil pero fuera de horario
    if es_dia_habil(fecha_actual):
        if fecha_actual.hour < HORA_INICIO_LABORAL:
            # Mismo día, a las 8 AM
            return fecha_actual.replace(hour=HORA_INICIO_LABORAL, minute=0, second=0, microsecond=0)
        elif fecha_actual.hour >= HORA_FIN_LABORAL:
            # Próximo día hábil a las 8 AM
            pass  # Continúa con la lógica de siguiente día hábil
    
    # Buscar el próximo día hábil
    dias_adelante = 1
    while dias_adelante <= 7:  # Máximo una semana
        fecha_futura = fecha_actual.replace(hour=HORA_INICIO_LABORAL, minute=0, second=0, microsecond=0)
        fecha_futura = fecha_futura.replace(day=fecha_actual.day + dias_adelante)
        
        if es_dia_habil(fecha_futura):
            return fecha_futura
        
        dias_adelante += 1
    
    # Fallback: mañana a las 8 AM
    return fecha_actual.replace(hour=HORA_INICIO_LABORAL, minute=0, second=0, microsecond=0, day=fecha_actual.day + 1)


def get_info_horario_laboral() -> dict:
    """
    Obtiene información completa sobre el estado del horario laboral.
    
    Returns:
        dict: Información detallada del horario laboral
    """
    fecha_actual = _get_datetime_colombia()
    debe_ejecutar, razon = debe_ejecutar_bot()
    
    info = {
        "fecha_actual": fecha_actual.strftime("%A %d/%m/%Y %H:%M:%S"),
        "debe_ejecutar": debe_ejecutar,
        "razon": razon,
        "es_dia_habil": es_dia_habil(fecha_actual),
        "es_horario_laboral": es_horario_laboral(fecha_actual),
        "configuracion": {
            "habilitado": ENABLE_HORARIO_LABORAL,
            "hora_inicio": f"{HORA_INICIO_LABORAL}:00",
            "hora_fin": f"{HORA_FIN_LABORAL}:00",
            "dias_habiles": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
            "validar_festivos": ENABLE_VALIDACION_FESTIVOS,
            "zona_horaria": TIMEZONE_COLOMBIA
        }
    }
    
    if not debe_ejecutar:
        proximo = get_proximo_horario_laboral()
        info["proximo_horario_laboral"] = proximo.strftime("%A %d/%m/%Y %H:%M")
    
    return info
