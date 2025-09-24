# crear_tarea_avanzada.ps1
<#
.SYNOPSIS
    Script avanzado para crear tarea automática del Bot de Memoriales en Windows Task Scheduler

.DESCRIPTION
    Crea una tarea programada que ejecuta el bot cada 5 minutos con configuración avanzada:
    - Reinicio automático en caso de fallo
    - Logging detallado
    - Configuración de seguridad
    - Validación de prerrequisitos

.PARAMETER TaskName
    Nombre de la tarea (por defecto: BotMemorialesAutomatico)

.PARAMETER Interval
    Intervalo en minutos entre ejecuciones (por defecto: 5)

.EXAMPLE
    .\crear_tarea_avanzada.ps1
    .\crear_tarea_avanzada.ps1 -TaskName "MiBot" -Interval 10
#>

param(
    [string]$TaskName = "BotMemorialesAutomatico",
    [int]$Interval = 5
)

# Configuración
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot
$ExecuteScript = Join-Path $ProjectRoot "ejecutar_mejorado.bat"
$LogPath = Join-Path $ProjectRoot "logs"

Write-Host "=================================================================" -ForegroundColor Green
Write-Host "CREACION AVANZADA DE TAREA - BOT DE MEMORIALES" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
Write-Host ""

# Verificar prerrequisitos
Write-Host "Verificando prerrequisitos..." -ForegroundColor Yellow

# Verificar si se ejecuta como administrador
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "Haz clic derecho en PowerShell y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que existe el script de ejecución
if (-not (Test-Path $ExecuteScript)) {
    Write-Host "ERROR: No se encuentra el script ejecutar_mejorado.bat" -ForegroundColor Red
    Write-Host "Ruta buscada: $ExecuteScript" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que el servicio Task Scheduler está ejecutándose
$taskService = Get-Service -Name "Schedule" -ErrorAction SilentlyContinue
if ($taskService.Status -ne "Running") {
    Write-Host "ERROR: El servicio Programador de tareas no está ejecutándose" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✓ Prerrequisitos verificados correctamente" -ForegroundColor Green
Write-Host ""

# Mostrar configuración
Write-Host "Configuración de la tarea:" -ForegroundColor Cyan
Write-Host "  Nombre: $TaskName"
Write-Host "  Script: $ExecuteScript"
Write-Host "  Intervalo: $Interval minutos"
Write-Host "  Logs: $LogPath"
Write-Host ""

# Confirmar creación
$confirm = Read-Host "¿Deseas crear la tarea con esta configuración? (S/N)"
if ($confirm -notmatch "^[Ss]$") {
    Write-Host "Operación cancelada por el usuario" -ForegroundColor Yellow
    exit 0
}

try {
    # Eliminar tarea existente si existe
    Write-Host "Eliminando tarea existente (si existe)..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

    # Crear acción de la tarea
    $action = New-ScheduledTaskAction -Execute $ExecuteScript -WorkingDirectory $ProjectRoot

    # Crear trigger (cada X minutos, indefinidamente)
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $Interval) -RepetitionDuration ([TimeSpan]::MaxValue)

    # Configuración de la tarea
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -DontStopOnIdleEnd -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

    # Principal (ejecutar con privilegios más altos)
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

    # Crear la tarea
    Write-Host "Creando tarea programada..." -ForegroundColor Yellow
    $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Bot automatizado de Memoriales - Ejecuta cada $Interval minutos con validación de horario laboral"

    # Registrar la tarea
    Register-ScheduledTask -TaskName $TaskName -InputObject $task -Force

    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "TAREA CREADA EXITOSAMENTE" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Detalles de la tarea:" -ForegroundColor Cyan
    Write-Host "  ✓ Nombre: $TaskName"
    Write-Host "  ✓ Frecuencia: Cada $Interval minutos"
    Write-Host "  ✓ Ejecución: 24/7 (bot valida horario internamente)"
    Write-Host "  ✓ Usuario: SYSTEM (privilegios elevados)"
    Write-Host "  ✓ Reinicio automático: Sí (hasta 3 intentos)"
    Write-Host ""
    Write-Host "Características del bot:" -ForegroundColor Cyan
    Write-Host "  • Solo procesa en horario laboral (8am-5pm)"
    Write-Host "  • Solo días hábiles de Colombia (Lun-Vie)"
    Write-Host "  • Excluye festivos colombianos"
    Write-Host "  • Logs organizados por fecha en logs/DDMMAAAA/"
    Write-Host ""
    Write-Host "Comandos útiles:" -ForegroundColor Yellow
    Write-Host "  Ver estado:    Get-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Ejecutar ahora: Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Deshabilitar:  Disable-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Habilitar:     Enable-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Eliminar:      Unregister-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    Write-Host "La tarea también se puede administrar desde:" -ForegroundColor Cyan
    Write-Host "Inicio > Administrador de tareas > Biblioteca del Programador de tareas"
    Write-Host ""

    # Mostrar estado actual
    $createdTask = Get-ScheduledTask -TaskName $TaskName
    Write-Host "Estado actual: $($createdTask.State)" -ForegroundColor Green

    # Opción de ejecutar inmediatamente
    Write-Host ""
    $runNow = Read-Host "¿Deseas ejecutar la tarea ahora para probar? (S/N)"
    if ($runNow -match "^[Ss]$") {
        Write-Host "Ejecutando tarea..." -ForegroundColor Yellow
        Start-ScheduledTask -TaskName $TaskName
        Write-Host "✓ Tarea ejecutada. Revisa los logs para ver el resultado." -ForegroundColor Green
    }

} catch {
    Write-Host ""
    Write-Host "ERROR: No se pudo crear la tarea" -ForegroundColor Red
    Write-Host "Detalles del error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Posibles soluciones:" -ForegroundColor Cyan
    Write-Host "1. Verificar que se ejecuta como Administrador"
    Write-Host "2. Comprobar que el servicio Task Scheduler está ejecutándose"
    Write-Host "3. Verificar permisos del usuario actual"
    Write-Host "4. Intentar desde una sesión de PowerShell elevada"
}

Write-Host ""
Read-Host "Presiona Enter para salir"
