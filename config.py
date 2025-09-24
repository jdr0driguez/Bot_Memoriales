# SERVIDOR SSH
HOST = "10.155.1.23"
PORT = 22
USERNAME = "Administrador"
PASSWORD = "d2GL3uYTLr5M"
KEYHASH = "3NcR1p+¡OnP4s$W0rDN@m3k3yV@lv3C0mP4NYC|B3RG3$+!0NM0DVL0|CB4CK3NDW3B"

# CONFIGURACIÓN DE LOGGING
# Controla si se muestran los logs de nivel DEBUG
# True = Mostrar logs DEBUG (más verboso)
# False = Ocultar logs DEBUG (solo INFO, WARNING, ERROR, CRITICAL)
ENABLE_DEBUG_LOGS = True

# Nivel mínimo de logging cuando DEBUG está desactivado
# Opciones: "INFO", "WARNING", "ERROR", "CRITICAL"
MIN_LOG_LEVEL_WHEN_DEBUG_OFF = "INFO"

# CONFIGURACIÓN DE LIMPIEZA DE LOGS
# Número de días de logs a mantener (0 = no limpiar automáticamente)
DIAS_LOGS_MANTENER = 7

# Habilitar limpieza automática de logs antiguos al iniciar
ENABLE_AUTO_CLEANUP_LOGS = True

# CONFIGURACIÓN DE HORARIO LABORAL
# Habilitar validación de horario laboral (solo ejecutar en horario de oficina)
ENABLE_HORARIO_LABORAL = True

# Horario de ejecución (formato 24 horas)
HORA_INICIO_LABORAL = 8   # 8:00 AM
HORA_FIN_LABORAL = 17     # 5:00 PM

# Días hábiles (0=Lunes, 1=Martes, 2=Miércoles, 3=Jueves, 4=Viernes, 5=Sábado, 6=Domingo)
DIAS_HABILES = [0, 1, 2, 3, 4]  # Lunes a Viernes

# Zona horaria de Colombia
TIMEZONE_COLOMBIA = "America/Bogota"

# Habilitar validación de festivos colombianos
ENABLE_VALIDACION_FESTIVOS = True