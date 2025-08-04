# 🚀 Guía de Ejecución en Bucle - Automatización de Memoriales

## 📋 Descripción

Esta automatización está configurada para ejecutarse en un bucle infinito cada 5 minutos, procesando expedientes pendientes automáticamente.

## 🛠️ Scripts Disponibles

### 1. `ejecutar.bat` (Recomendado para Windows)
- **Uso**: Doble clic o ejecutar desde línea de comandos
- **Características**:
  - Bucle infinito cada 5 minutos
  - Contador regresivo visual
  - Manejo básico de errores
  - Logs en consola

### 2. `ejecutar_mejorado.bat` (Versión avanzada)
- **Uso**: Doble clic o ejecutar desde línea de comandos
- **Características**:
  - Logs detallados en archivo `logs\ejecucion_automatizacion.log`
  - Mejor manejo de errores
  - Verificación de entorno virtual
  - Contador de ciclos

### 3. `ejecutar.ps1` (PowerShell - Más robusto)
- **Uso**: `powershell -ExecutionPolicy Bypass -File ejecutar.ps1`
- **Características**:
  - Script de PowerShell más robusto
  - Logs detallados
  - Manejo avanzado de excepciones
  - Parámetros configurables

## 🚀 Cómo Ejecutar

### Opción 1: Script Batch Básico
```bash
# Doble clic en ejecutar.bat
# O desde línea de comandos:
ejecutar.bat
```

### Opción 2: Script Batch Mejorado
```bash
# Doble clic en ejecutar_mejorado.bat
# O desde línea de comandos:
ejecutar_mejorado.bat
```

### Opción 3: Script PowerShell
```powershell
# Desde PowerShell:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1

# Con parámetros personalizados:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1 -IntervaloMinutos 10
```

## ⚙️ Configuración

### Cambiar Intervalo de Ejecución

#### En `ejecutar.bat`:
```batch
SET INTERVALO_MINUTOS=10  # Cambiar a 10 minutos
```

#### En `ejecutar_mejorado.bat`:
```batch
SET INTERVALO_MINUTOS=10  # Cambiar a 10 minutos
```

#### En `ejecutar.ps1`:
```powershell
# Al ejecutar:
powershell -ExecutionPolicy Bypass -File ejecutar.ps1 -IntervaloMinutos 10
```

## 📊 Monitoreo

### Logs Disponibles

1. **Logs de la automatización**: `logs\WS_RNEC.log`
2. **Logs de ejecución del script**: 
   - `logs\ejecucion_automatizacion.log` (ejecutar_mejorado.bat)
   - `logs\ejecucion_powershell.log` (ejecutar.ps1)

### Códigos de Salida

- **0**: Proceso completado exitosamente
- **1**: Sin expedientes para procesar
- **Otros**: Errores durante la ejecución

## 🔄 Flujo de Ejecución

```
1. Inicialización
   ├── Crear entorno virtual (si no existe)
   ├── Activar entorno virtual
   └── Instalar dependencias

2. Bucle Principal
   ├── Ejecutar main.py
   ├── Procesar expedientes pendientes
   ├── Actualizar estados exitosos
   └── Esperar 5 minutos

3. Repetir indefinidamente
```

## 🛑 Cómo Detener

### Detener el Proceso
- **Ctrl+C**: Detener inmediatamente
- **Cerrar ventana**: Detener el script

### Reiniciar Automáticamente
Para que el script se reinicie automáticamente en caso de error, puedes usar:

```batch
:reinicio
ejecutar_mejorado.bat
if %ERRORLEVEL% NEQ 0 (
    echo Error detectado, reiniciando en 30 segundos...
    timeout /t 30 /nobreak >nul
    goto reinicio
)
```

## 📈 Monitoreo Avanzado

### Verificar Estado del Proceso
```bash
# Verificar si está ejecutándose
tasklist /FI "IMAGENAME eq python.exe"

# Ver logs en tiempo real
Get-Content logs\ejecucion_automatizacion.log -Wait
```

### Configurar como Servicio Windows
Para ejecutar como servicio de Windows, puedes usar herramientas como:
- **NSSM** (Non-Sucking Service Manager)
- **Windows Task Scheduler**

## 🔧 Troubleshooting

### Problemas Comunes

1. **Error de entorno virtual**:
   ```bash
   # Eliminar y recrear
   rmdir /s vScrap
   python -m venv vScrap
   ```

2. **Error de dependencias**:
   ```bash
   # Reinstalar dependencias
   pip install -r requirements.txt --force-reinstall
   ```

3. **Error de permisos**:
   - Ejecutar como administrador
   - Verificar permisos de escritura en logs/

### Logs de Depuración

Los logs detallados se encuentran en:
- `logs\WS_RNEC.log` - Logs de la automatización
- `logs\ejecucion_automatizacion.log` - Logs del script de ejecución

## 📝 Notas Importantes

- ✅ El script maneja automáticamente expedientes sin procesar
- ✅ Actualiza estados de expedientes procesados exitosamente
- ✅ Logs detallados para seguimiento
- ✅ Manejo robusto de errores
- ✅ Configuración flexible de intervalos

- ⚠️ Asegúrate de tener Python instalado
- ⚠️ Verifica la conectividad de red para las APIs
- ⚠️ Monitorea el espacio en disco para los logs 