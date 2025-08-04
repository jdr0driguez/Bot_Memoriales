# 🤖 Automatización de Memoriales - Bot RNEC

## 📋 Descripción General

Sistema automatizado para el procesamiento de memoriales judiciales que incluye:
- **Consumo de APIs** para obtener expedientes pendientes
- **Procesamiento automático** de documentos y envío de correos
- **Validación de campos obligatorios** (CorreoPass, CorreoRemitente)
- **Actualización de estados** de expedientes procesados
- **Ejecución en bucle infinito** cada 5 minutos
- **Sistema de logging completo** con rotación diaria

## 🏗️ Arquitectura del Proyecto

```
Bot_MemorialesFinal/
├── core/                          # Módulos principales
│   ├── API_Consumo.py            # Consumo de APIs y procesamiento principal
│   ├── API_Modelos.py            # Modelos de datos (dataclasses)
│   ├── API_parser.py             # Parser de respuestas de API
│   ├── processing_service.py     # Lógica de procesamiento de expedientes
│   ├── estado_service.py         # Actualización de estados de expedientes
│   ├── db_Connection.py          # Conexión a base de datos SQL Server
│   ├── repository.py             # Consultas a base de datos
│   ├── email_service.py          # Envío de correos electrónicos
│   ├── descargaPlantillaSFTP.py  # Descarga de archivos via SFTP
│   └── dcryptCsharp.py          # Desencriptación AES compatible con C#
├── tests/                        # Tests unitarios
│   ├── test_consumo.py          # Test de consumo de API
│   ├── test_estado_service.py   # Test de actualización de estados
│   └── test_validaciones.py     # Test de validaciones de campos
├── logs/                         # Archivos de logs (generados automáticamente)
├── vScrap/                       # Entorno virtual Python
├── ejecutar.bat                  # Script de ejecución básico
├── ejecutar_mejorado.bat         # Script de ejecución avanzado
├── ejecutar.ps1                  # Script PowerShell
├── main.py                       # Punto de entrada principal
├── logger.py                     # Configuración del sistema de logging
├── config.py                     # Configuraciones del sistema
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
Editar `config.py` con tus credenciales:
```python
# Configuración de base de datos
DB_SERVER = "tu_servidor"
DB_DATABASE = "tu_base_datos"
DB_USERNAME = "tu_usuario"
DB_PASSWORD = "tu_password"

# Configuración SFTP
SFTP_HOST = "tu_host_sftp"
SFTP_USERNAME = "tu_usuario_sftp"
SFTP_PASSWORD = "tu_password_sftp"

# Configuración de correo
SMTP_SERVER = "tu_servidor_smtp"
SMTP_PORT = 587

# Clave de desencriptación
KEYHASH = "tu_clave_hash"
```

## 🔧 Funcionalidades Principales

### 1. Consumo de APIs
- **Endpoint**: `http://10.155.1.43/backend/api/Externo/bot-plantillas-pendiente`
- **Función**: Obtiene expedientes pendientes de procesamiento
- **Validación**: Campos obligatorios (CorreoPass, CorreoRemitente)

### 2. Procesamiento de Expedientes
```python
# Flujo de procesamiento
1. Validar campos obligatorios
2. Consultar base de datos
3. Descargar archivo PDF via SFTP
4. Desencriptar contraseña de correo
5. Enviar correo con adjunto
6. Actualizar estado del expediente
```

### 3. Sistema de Logging
- **Rotación diaria** de archivos de log
- **Separación por niveles** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Log combinado** para seguimiento completo
- **Sin emojis** para compatibilidad con terminales

### 4. Validaciones Implementadas
- ✅ **CorreoPass**: Campo obligatorio para desencriptación
- ✅ **CorreoRemitente**: Campo obligatorio para envío
- ✅ **Tipo de proceso**: Solo procesa IdTipoProceso = 1
- ✅ **Existencia de registros** en base de datos

### 5. Actualización de Estados
- **Endpoint**: `https://rocketvel.ai/backend/api/Externo/expediente-estadobotplantilla`
- **Método**: PUT
- **Payload**: 
```json
{
  "ExpedientesPlantillas": [
    {
      "ExpedienteId": "ID_DEL_EXPEDIENTE",
      "PlantillaId": "ID_DE_LA_PLANTILLA"
    }
  ],
  "Estado": "Terminado"
}
```

## 📊 Scripts de Ejecución

### Opción 1: Script Básico
```bash
# Doble clic en ejecutar.bat
# Ejecuta en bucle cada 5 minutos
```

### Opción 2: Script Mejorado (Recomendado)
```bash
# Doble clic en ejecutar_mejorado.bat
# Incluye logs detallados y mejor manejo de errores
```

### Opción 3: PowerShell
```powershell
# Desde PowerShell:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1

# Con intervalo personalizado:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1 -IntervaloMinutos 10
```

## 📝 Logs y Monitoreo

### Archivos de Log
- **`logs/WS_RNEC.log`**: Log combinado de toda la automatización
- **`logs/debug.log`**: Logs de nivel DEBUG
- **`logs/info.log`**: Logs de nivel INFO
- **`logs/warning.log`**: Logs de nivel WARNING
- **`logs/error.log`**: Logs de nivel ERROR
- **`logs/critical.log`**: Logs de nivel CRITICAL
- **`logs/ejecucion_automatizacion.log`**: Logs del script de ejecución

### Ejemplo de Logs
```
[2024-01-15 10:30:15] [INFO] [API_Consumo] Iniciando consumo de API para plantillas pendientes
[2024-01-15 10:30:16] [INFO] [API_Consumo] Procesando 3 elemento(s) de la API
[2024-01-15 10:30:17] [INFO] [ProcessingService] Iniciando procesamiento del expediente 12345
[2024-01-15 10:30:20] [INFO] [EmailService] Correo enviado exitosamente para expediente 12345
[2024-01-15 10:30:21] [INFO] [EstadoService] Estado actualizado exitosamente para expediente 12345
```

## 🧪 Tests Disponibles

### Ejecutar Tests
```bash
# Test de consumo de API
python tests/test_consumo.py

# Test de actualización de estados
python tests/test_estado_service.py

# Test de validaciones
python tests/test_validaciones.py
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
- **Otros**: Errores durante la ejecución

## 🔧 Troubleshooting

### Problemas Comunes

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
- Sistema de logging completo sin emojis
- Validación de campos obligatorios
- Actualización automática de estados
- Ejecución en bucle infinito
- Manejo robusto de errores
- Tests unitarios incluidos

### ⚠️ Consideraciones
- Asegúrate de tener Python instalado
- Verifica conectividad de red
- Monitorea espacio en disco para logs
- Configura credenciales correctamente
- Prueba en ambiente de desarrollo primero

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

**Versión**: 1.0.0  
**Última actualización**: Enero 2024  
**Autor**: Equipo de Desarrollo