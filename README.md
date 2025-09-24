# 🤖 Automatización de Memoriales - Bot RNEC

## 📋 Descripción General

Sistema automatizado avanzado para el procesamiento de memoriales judiciales que incluye:
- **🕐 Horario Laboral Inteligente**: Solo ejecuta en días hábiles de Colombia (8am-5pm)
- **📅 Validación de Festivos**: Reconoce festivos colombianos automáticamente
- **🔄 Consumo de APIs** para obtener expedientes pendientes
- **📧 Procesamiento automático** de documentos y envío de correos
- **✅ Validación robusta** de campos obligatorios y correos válidos
- **🔄 Actualización de estados** de expedientes procesados
- **🗂️ Logs organizados por fecha** con limpieza automática
- **🎛️ Control granular de DEBUG** logs configurable
- **🧹 Limpieza automática** de archivos descargados
- **⚙️ Automatización completa** con Windows Task Scheduler

## 🏗️ Arquitectura del Proyecto

```
Bot_MemorialesFinal/
├── core/                          # Módulos principales
│   ├── API_Consumo.py            # Consumo de APIs y procesamiento principal
│   ├── API_Modelos.py            # Modelos de datos (dataclasses)
│   ├── API_parser.py             # Parser de respuestas de API
│   ├── processing_service.py     # Lógica de procesamiento + limpieza archivos
│   ├── estado_service.py         # Actualización de estados de expedientes
│   ├── horario_laboral.py        # 🆕 Validación horario laboral y festivos
│   ├── db_Connection.py          # Conexión a base de datos SQL Server
│   ├── repository.py             # Consultas a base de datos
│   ├── email_service.py          # Envío de correos electrónicos
│   ├── descargaPlantillaSFTP.py  # Descarga de archivos via SFTP
│   └── dcryptCsharp.py          # Desencriptación AES compatible con C#
├── automatizacion/               # 🆕 Scripts de automatización Windows
│   ├── crear_tarea_windows.bat   # Crear tarea en Task Scheduler (básico)
│   ├── crear_tarea_avanzada.ps1  # Crear tarea avanzada (PowerShell)
│   └── gestionar_tarea.bat       # Gestionar tarea existente
├── tests/                        # Tests unitarios expandidos
│   ├── test_consumo.py          # Test de consumo de API
│   ├── test_estado_service.py   # Test de actualización de estados
│   ├── test_validaciones.py     # Test de validaciones de campos
│   ├── test_limpieza_archivos.py # 🆕 Test limpieza automática archivos
│   ├── test_config_debug_logs.py # 🆕 Test control logs DEBUG
│   ├── test_logs_por_fecha.py   # 🆕 Test organización logs por fecha
│   └── test_horario_laboral.py  # 🆕 Test validación horario laboral
├── logs/                         # 🆕 Logs organizados por fecha
│   ├── 24092025/                # Logs del 24/09/2025
│   │   ├── WS_RNEC.log          # Log combinado
│   │   ├── debug.log            # Solo DEBUG (configurable)
│   │   ├── info.log             # Solo INFO
│   │   ├── warning.log          # Solo WARNING
│   │   ├── error.log            # Solo ERROR
│   │   └── critical.log         # Solo CRITICAL
│   └── (logs antiguos eliminados automáticamente)
├── vScrap_clean/                 # Entorno virtual Python
├── ejecutar.bat                  # Script de ejecución básico
├── ejecutar_mejorado.bat         # Script de ejecución avanzado
├── ejecutar.ps1                  # Script PowerShell
├── main.py                       # 🆕 Punto de entrada con validación horario
├── logger.py                     # 🆕 Sistema logging avanzado por fechas
├── config.py                     # 🆕 Configuraciones expandidas
└── requirements.txt              # Dependencias del proyecto
```

## 🚀 Inicio Rápido

### 1. Requisitos Previos
- Python 3.8 o superior
- Acceso a SQL Server
- Credenciales SFTP
- Configuración de correo electrónico

### 2. Instalación
```bash
# Clonar o descargar el proyecto
cd Bot_MemorialesFinal

# Ejecutar el script de automatización
ejecutar_mejorado.bat
```

### 3. Configuración

Editar `config.py` con tus credenciales y preferencias:

```python
# SERVIDOR SSH/SFTP
HOST = "10.155.1.23"
PORT = 22
USERNAME = "tu_usuario_sftp"
PASSWORD = "tu_password_sftp"
KEYHASH = "tu_clave_desencriptacion"

# 🆕 CONFIGURACIÓN DE LOGGING
ENABLE_DEBUG_LOGS = True              # True/False para mostrar logs DEBUG
MIN_LOG_LEVEL_WHEN_DEBUG_OFF = "INFO" # Nivel mínimo cuando DEBUG está off
DIAS_LOGS_MANTENER = 7                # Días de logs a mantener
ENABLE_AUTO_CLEANUP_LOGS = True       # Limpieza automática de logs antiguos

# 🆕 CONFIGURACIÓN DE HORARIO LABORAL
ENABLE_HORARIO_LABORAL = True         # Validar horario laboral
HORA_INICIO_LABORAL = 8               # 8:00 AM
HORA_FIN_LABORAL = 17                 # 5:00 PM
DIAS_HABILES = [0, 1, 2, 3, 4]        # Lunes a Viernes
TIMEZONE_COLOMBIA = "America/Bogota"   # Zona horaria Colombia
ENABLE_VALIDACION_FESTIVOS = True     # Validar festivos colombianos
```

### 4. Automatización Completa (Recomendado)

Para automatización 24/7 en servidor Windows:

```bash
# Opción 1: Script básico (como Administrador)
cd automatizacion
crear_tarea_windows.bat

# Opción 2: Script avanzado PowerShell (como Administrador)
cd automatizacion
powershell -ExecutionPolicy Bypass -File crear_tarea_avanzada.ps1

# Gestionar tarea existente
gestionar_tarea.bat
```

## 🔧 Funcionalidades Principales

### 1. 🕐 Horario Laboral Inteligente (NUEVO)
- **Validación automática**: Solo ejecuta en días hábiles de Colombia
- **Horario**: 8:00 AM - 5:00 PM (configurable)
- **Días hábiles**: Lunes a Viernes (configurable)
- **Festivos colombianos**: Reconocimiento automático de festivos
- **Zona horaria**: America/Bogota
- **Logs informativos**: Próxima ejecución programada cuando está fuera de horario

### 2. 🔄 Consumo de APIs
- **Endpoint**: `https://rocketvel.ai/backend/api/Externo/bot-plantillas-pendiente`
- **Función**: Obtiene expedientes pendientes de procesamiento
- **Validación robusta**: Campos obligatorios y formato de correos
- **Manejo de errores**: Logs limpios sin mensajes técnicos extensos

### 3. 📧 Procesamiento Avanzado de Expedientes
```python
# Flujo de procesamiento mejorado
1. ✅ Validar horario laboral (días hábiles + horario)
2. ✅ Validar campos obligatorios (CorreoPass, CorreoRemitente)
3. ✅ Validar formato de correo del juzgado
4. ✅ Consultar base de datos
5. ✅ Descargar archivo PDF via SFTP (si es necesario)
6. ✅ Desencriptar contraseña de correo
7. ✅ Enviar correo con/sin adjunto
8. ✅ Limpiar archivo descargado automáticamente
9. ✅ Actualizar estado del expediente
```

### 4. 🗂️ Sistema de Logging Avanzado (NUEVO)
- **Organización por fecha**: `logs/DDMMAAAA/` (ej: `logs/24092025/`)
- **Limpieza automática**: Elimina logs antiguos según configuración
- **Control de DEBUG**: Activar/desactivar logs DEBUG desde config
- **Separación por niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log combinado**: WS_RNEC.log con todos los niveles
- **Rotación inteligente**: Mantiene N días configurables

### 5. 🧹 Limpieza Automática de Archivos (NUEVO)
- **Limpieza post-envío**: Elimina archivos PDF después del envío exitoso
- **Limpieza en errores**: Elimina archivos incluso si falla el envío
- **Manejo seguro**: No interrumpe el flujo principal si falla la limpieza
- **Logs detallados**: Seguimiento de todas las operaciones de limpieza

### 6. ✅ Validaciones Robustas Implementadas
- ✅ **Horario laboral**: Solo días hábiles de Colombia (8am-5pm)
- ✅ **Festivos colombianos**: Validación automática de festivos
- ✅ **CorreoPass**: Campo obligatorio para desencriptación
- ✅ **CorreoRemitente**: Campo obligatorio para envío
- ✅ **Correo del juzgado**: Validación de formato y valores válidos
- ✅ **Tipo de proceso**: Solo procesa IdTipoProceso = 1
- ✅ **Existencia de registros** en base de datos
- ✅ **Archivos SFTP**: Validación antes de descarga

### 7. 🔄 Actualización de Estados
- **Endpoint**: `https://rocketvel.ai/backend/api/Externo/expediente-estadobotplantilla`
- **Método**: PUT
- **Actualización masiva**: Procesa múltiples expedientes exitosos
- **Payload mejorado**: 
```json
{
  "ExpedientesPlantillas": [
    {
      "ExpedienteId": "ID_DEL_EXPEDIENTE",
      "PlantillaId": "ID_DE_LA_PLANTILLA",
      "DemandadoId": "ID_DEL_DEMANDADO"
    }
  ],
  "Estado": "Terminado"
}
```

### 8. ⚙️ Automatización Completa Windows (NUEVO)
- **Task Scheduler**: Integración nativa con Windows
- **Ejecución 24/7**: El bot valida horario internamente
- **Reinicio automático**: En caso de fallos
- **Privilegios elevados**: Ejecución como SYSTEM
- **Gestión avanzada**: Scripts para administrar la tarea

## 📊 Opciones de Ejecución

### 🚀 Opción 1: Automatización Completa (RECOMENDADO)
```bash
# Para servidores Windows - Configuración 24/7
cd automatizacion

# Script básico (como Administrador)
crear_tarea_windows.bat

# Script avanzado PowerShell (como Administrador)
powershell -ExecutionPolicy Bypass -File crear_tarea_avanzada.ps1

# Gestionar tarea existente
gestionar_tarea.bat
```

**Características de la automatización:**
- ✅ Ejecuta cada 5 minutos automáticamente
- ✅ Solo procesa en horario laboral (8am-5pm, días hábiles)
- ✅ Reinicio automático en caso de fallos
- ✅ Ejecución con privilegios elevados
- ✅ Gestión completa desde Task Scheduler

### 🔧 Opción 2: Ejecución Manual

#### Script Básico
```bash
# Doble clic en ejecutar.bat
# Ejecuta en bucle cada 5 minutos (manual)
```

#### Script Mejorado
```bash
# Doble clic en ejecutar_mejorado.bat
# Incluye logs detallados y mejor manejo de errores
```

#### PowerShell
```powershell
# Desde PowerShell:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1

# Con intervalo personalizado:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1 -IntervaloMinutos 10
```

## 📝 Sistema de Logs Avanzado

### 🗂️ Organización por Fecha (NUEVO)
```
logs/
├── 22092025/          # Logs del 22/09/2025
│   ├── WS_RNEC.log    # Log combinado
│   ├── debug.log      # Solo DEBUG (configurable)
│   ├── info.log       # Solo INFO
│   ├── warning.log    # Solo WARNING
│   ├── error.log      # Solo ERROR
│   └── critical.log   # Solo CRITICAL
├── 23092025/          # Logs del 23/09/2025
├── 24092025/          # Logs del 24/09/2025 (hoy)
└── (logs antiguos eliminados automáticamente)
```

### ⚙️ Control de Logs DEBUG
```python
# En config.py
ENABLE_DEBUG_LOGS = True   # Mostrar logs DEBUG (desarrollo)
ENABLE_DEBUG_LOGS = False  # Ocultar logs DEBUG (producción)
```

### 🧹 Limpieza Automática
```python
# En config.py
DIAS_LOGS_MANTENER = 7           # Mantener 7 días de logs
ENABLE_AUTO_CLEANUP_LOGS = True  # Limpieza automática habilitada
```

### 📋 Ejemplo de Logs Mejorados
```
[2025-09-24 08:15:00] [INFO] [Main] Validación de horario laboral: Horario laboral válido: Martes 24/09/2025 08:15
[2025-09-24 08:15:01] [INFO] [API_Consumo] Iniciando consumo de API para plantillas pendientes
[2025-09-24 08:15:02] [INFO] [API_Consumo] Procesando 3 elemento(s) de la API
[2025-09-24 08:15:03] [INFO] [ProcessingService] Iniciando procesamiento del expediente ALI-0026922
[2025-09-24 08:15:04] [INFO] [ProcessingService] Correo del juzgado válido encontrado: juzgado@ejemplo.gov.co
[2025-09-24 08:15:05] [INFO] [ProcessingService] Archivo descargado exitosamente: documento.pdf
[2025-09-24 08:15:06] [INFO] [EmailService] Correo enviado exitosamente para expediente ALI-0026922
[2025-09-24 08:15:07] [INFO] [ProcessingService] Archivo local eliminado exitosamente: documento.pdf
[2025-09-24 08:15:08] [INFO] [EstadoService] Estado actualizado exitosamente para expediente ALI-0026922
```

### 🕐 Logs de Horario Laboral
```
# Fuera de horario laboral
[2025-09-24 19:30:00] [INFO] [Main] Bot no ejecutado - Fuera de horario laboral
[2025-09-24 19:30:00] [INFO] [Main] Próxima ejecución programada: Miércoles 25/09/2025 08:00

# Fin de semana o festivo
[2025-09-28 10:00:00] [INFO] [Main] Bot no ejecutado: No es día hábil: Sábado 28/09/2025 (fin de semana)
```

## 🧪 Tests Disponibles

### 🔬 Tests Principales
```bash
# Test de consumo de API
python tests/test_consumo.py

# Test de actualización de estados
python tests/test_estado_service.py

# Test de validaciones de campos
python tests/test_validaciones.py
```

### 🆕 Tests de Nuevas Funcionalidades
```bash
# Test de limpieza automática de archivos
python tests/test_limpieza_archivos.py

# Test de control de logs DEBUG
python tests/test_config_debug_logs.py

# Test de organización de logs por fecha
python tests/test_logs_por_fecha.py

# Test de validación de horario laboral
python tests/test_horario_laboral.py

# Test de validación de correos del juzgado
python tests/test_validacion_correo_juzgado.py
```

### 🏃‍♂️ Ejecutar Todos los Tests
```bash
# Ejecutar todos los tests disponibles
python -m unittest discover tests/ -v
```

## ⚙️ Configuración Avanzada

### Cambiar Intervalo de Ejecución
```batch
# En ejecutar_mejorado.bat
SET INTERVALO_MINUTOS=10  # Cambiar a 10 minutos
```

### Configurar Logs
```python
# En logger.py
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
```

### Configurar Rotación de Logs
```python
# En logger.py
backupCount=7  # Mantener 7 días de logs
```

## 🔄 Flujo Completo de Ejecución

```
1. Inicialización del Sistema
   ├── Crear/activar entorno virtual
   ├── Instalar dependencias
   └── Configurar sistema de logging

2. Bucle Principal (cada 5 minutos)
   ├── Consumir API de expedientes pendientes
   ├── Validar campos obligatorios
   ├── Procesar cada expediente:
   │   ├── Consultar base de datos
   │   ├── Descargar archivo PDF
   │   ├── Desencriptar contraseña
   │   ├── Enviar correo electrónico
   │   └── Actualizar estado
   └── Esperar 5 minutos

3. Logs y Monitoreo
   ├── Logs detallados por módulo
   ├── Rotación diaria de archivos
   └── Seguimiento de errores
```

## 🛑 Códigos de Salida

- **0**: Proceso completado exitosamente
- **1**: Sin expedientes para procesar
- **2**: 🆕 Fuera de horario laboral (días no hábiles o fuera de 8am-5pm)
- **Otros**: Errores durante la ejecución

### 📊 Interpretación de Códigos
```bash
# Código 0 - Éxito
Bot ejecutado correctamente, expedientes procesados

# Código 1 - Sin trabajo
Bot ejecutado en horario laboral, pero no hay expedientes pendientes

# Código 2 - Fuera de horario
Bot no ejecutado por estar fuera del horario laboral configurado
- Fin de semana (Sábado/Domingo)
- Festivo colombiano
- Fuera del horario 8am-5pm
```

## 🆕 Mejoras Implementadas

### 🔧 Optimizaciones de Rendimiento
- **Limpieza automática de archivos**: Evita acumulación de PDFs descargados
- **Logs organizados por fecha**: Mejor gestión del espacio en disco
- **Validación temprana**: Evita procesamiento innecesario fuera de horario
- **Control de DEBUG**: Reduce I/O en producción

### 🛡️ Mejoras de Seguridad y Robustez
- **Validación de correos**: Evita intentos de envío a destinatarios inválidos
- **Manejo de errores mejorado**: Logs más claros y específicos
- **Limpieza en casos de error**: Archivos se eliminan incluso si falla el proceso
- **Validación de horario**: Solo ejecuta cuando es apropiado

### 🎛️ Mejoras de Configuración
- **Horario laboral configurable**: Adaptable a diferentes necesidades
- **Control granular de logs**: DEBUG activable/desactivable
- **Limpieza automática configurable**: Días de retención personalizables
- **Automatización completa**: Scripts para Windows Task Scheduler

## 🔧 Troubleshooting

### 🆕 Problemas de Horario Laboral
1. **Bot no ejecuta en horario laboral**:
   - Verificar `ENABLE_HORARIO_LABORAL = True` en config.py
   - Comprobar `HORA_INICIO_LABORAL` y `HORA_FIN_LABORAL`
   - Verificar zona horaria del servidor

2. **Bot ejecuta en festivos**:
   - Verificar `ENABLE_VALIDACION_FESTIVOS = True`
   - Comprobar que el año actual tiene festivos configurados

### 🗂️ Problemas de Logs
1. **Logs DEBUG no aparecen**:
   - Verificar `ENABLE_DEBUG_LOGS = True` en config.py
   - Reiniciar el bot para aplicar cambios

2. **Carpetas de logs no se crean**:
   - Verificar permisos de escritura en directorio logs/
   - Comprobar espacio disponible en disco

### 📧 Problemas de Correo Mejorados
1. **Error "Correo del juzgado no válido"**:
   - Verificar que el correo en BD no sea "NO ESPECIFICADO"
   - Comprobar formato válido de email (usuario@dominio.com)

2. **Archivos no se eliminan después del envío**:
   - Verificar permisos de escritura en directorio del bot
   - Comprobar logs para errores de limpieza

### 🔄 Problemas de Automatización
1. **Tarea de Windows no se ejecuta**:
   - Verificar que se creó como Administrador
   - Comprobar que el servicio Task Scheduler está ejecutándose
   - Verificar permisos del usuario SYSTEM

2. **Bot se ejecuta pero no procesa**:
   - Verificar horario laboral en logs
   - Comprobar códigos de salida (0=éxito, 1=sin trabajo, 2=fuera de horario)

### 🛠️ Problemas Tradicionales
1. **Error de conexión a base de datos**:
   - Verificar credenciales en `config.py`
   - Comprobar conectividad de red

2. **Error de SFTP**:
   - Verificar credenciales SFTP
   - Comprobar permisos de archivos

3. **Error de envío de correo**:
   - Verificar configuración SMTP
   - Comprobar credenciales de correo

4. **Error de desencriptación**:
   - Verificar KEYHASH en `config.py`
   - Comprobar formato de datos encriptados

### Logs de Depuración
```bash
# Ver logs en tiempo real
Get-Content logs\WS_RNEC.log -Wait

# Ver logs de ejecución del script
Get-Content logs\ejecucion_automatizacion.log -Wait
```

## 📈 Monitoreo Avanzado

### Verificar Estado del Proceso
```bash
# Verificar si está ejecutándose
tasklist /FI "IMAGENAME eq python.exe"

# Ver uso de recursos
Get-Process python
```

### Configurar como Servicio Windows
```bash
# Usando NSSM
nssm install "BotMemoriales" "C:\ruta\a\ejecutar_mejorado.bat"
nssm start "BotMemoriales"
```

## 📋 Dependencias

### Python Packages
```
requests>=2.25.1
pyodbc>=4.0.30
paramiko>=2.7.2
cryptography>=3.4.7
Pillow>=8.2.0
numpy>=1.21.0
opencv-python>=4.5.3
```

### Configuración de Sistema
- **Python**: 3.8+
- **SQL Server**: Driver ODBC
- **Red**: Acceso a APIs y SFTP
- **Permisos**: Escritura en directorio logs/

## 📝 Notas Importantes

### ✅ Características Implementadas
- 🕐 **Horario laboral inteligente** con validación de festivos colombianos
- 🗂️ **Sistema de logging avanzado** organizado por fechas con limpieza automática
- 🎛️ **Control granular de DEBUG** logs configurable desde config.py
- 🧹 **Limpieza automática** de archivos descargados (PDFs)
- ✅ **Validación robusta** de correos del juzgado y campos obligatorios
- 🔄 **Actualización masiva** de estados de expedientes
- ⚙️ **Automatización completa** con Windows Task Scheduler
- 🧪 **Suite completa de tests** para todas las funcionalidades
- 🛡️ **Manejo robusto de errores** con logs claros y específicos

### ⚠️ Consideraciones Importantes

#### 🖥️ Para Servidores Windows
- **Usar automatización completa**: Ejecutar scripts en `automatizacion/` como Administrador
- **Task Scheduler**: La mejor práctica para ejecución 24/7
- **Zona horaria**: Verificar que el servidor esté en zona horaria de Colombia

#### 🔧 Para Desarrollo
- **DEBUG habilitado**: `ENABLE_DEBUG_LOGS = True` para desarrollo
- **DEBUG deshabilitado**: `ENABLE_DEBUG_LOGS = False` para producción
- **Tests**: Ejecutar suite completa antes de desplegar

#### 📊 Para Monitoreo
- **Logs organizados**: Revisar carpeta `logs/DDMMAAAA/` del día actual
- **Códigos de salida**: 0=éxito, 1=sin trabajo, 2=fuera de horario
- **Limpieza automática**: Configurar `DIAS_LOGS_MANTENER` según necesidades

#### 🕐 Para Horario Laboral
- **Solo días hábiles**: Lunes a Viernes (configurable)
- **Solo horario laboral**: 8am-5pm (configurable)
- **Festivos colombianos**: Reconocimiento automático
- **Zona horaria**: America/Bogota

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Ejecuta los tests
5. Envía un pull request

## 📞 Soporte

Para soporte técnico o preguntas:
- Revisar logs en `logs/`
- Ejecutar tests para verificar funcionalidad
- Consultar documentación de APIs
- Verificar configuración en `config.py`

---

## 📈 Historial de Versiones

### v2.0.0 - Septiembre 2025 (ACTUAL)
- 🆕 **Horario laboral inteligente** con validación de festivos colombianos
- 🆕 **Logs organizados por fecha** con limpieza automática
- 🆕 **Control granular de DEBUG** logs configurable
- 🆕 **Limpieza automática** de archivos descargados
- 🆕 **Validación robusta** de correos del juzgado
- 🆕 **Automatización completa** con Windows Task Scheduler
- 🆕 **Suite expandida de tests** para todas las funcionalidades
- 🔧 **Mejoras de rendimiento** y manejo de errores

### v1.0.0 - Enero 2024
- ✅ Sistema básico de procesamiento de memoriales
- ✅ Consumo de APIs y envío de correos
- ✅ Sistema de logging básico
- ✅ Validaciones fundamentales

---

**Versión Actual**: 2.0.0  
**Última Actualización**: Septiembre 2025  
**Compatibilidad**: Windows Server 2016+, Python 3.8+  
**Autor**: Equipo de Desarrollo  

## 🎯 Próximas Mejoras Planificadas
- 📊 Dashboard web para monitoreo en tiempo real
- 🔔 Notificaciones por email/Slack para errores críticos
- 📱 API REST para gestión remota
- 🐳 Containerización con Docker
- ☁️ Soporte para Azure/AWS Task Scheduling