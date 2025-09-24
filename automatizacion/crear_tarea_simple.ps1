# crear_tarea_simple.ps1
<#
.SYNOPSIS
    Script simple para crear tarea automatica usando schtasks (mas compatible)

.DESCRIPTION
    Crea una tarea programada usando el comando schtasks nativo de Windows
    que es mas compatible con diferentes versiones de Windows

.PARAMETER TaskName
    Nombre de la tarea (por defecto: BotMemorialesAutomatico)

.PARAMETER Interval
    Intervalo en minutos entre ejecuciones (por defecto: 5)
#>

param(
    [string]$TaskName = "BotMemorialesAutomatico",
    [int]$Interval = 5
)

# Configuracion
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot
$ExecuteScript = Join-Path $ProjectRoot "ejecutar_mejorado.bat"

Write-Host "=================================================================" -ForegroundColor Green
Write-Host "CREACION SIMPLE DE TAREA - BOT DE MEMORIALES" -ForegroundColor Green
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

# Verificar que existe el script de ejecucion
if (-not (Test-Path $ExecuteScript)) {
    Write-Host "ERROR: No se encuentra el script ejecutar_mejorado.bat" -ForegroundColor Red
    Write-Host "Ruta buscada: $ExecuteScript" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Prerrequisitos verificados correctamente" -ForegroundColor Green
Write-Host ""

# Mostrar configuracion
Write-Host "Configuracion de la tarea:" -ForegroundColor Cyan
Write-Host "  Nombre: $TaskName"
Write-Host "  Script: $ExecuteScript"
Write-Host "  Intervalo: $Interval minutos"
Write-Host ""

# Confirmar creacion
$confirm = Read-Host "Deseas crear la tarea con esta configuracion? (S/N)"
if ($confirm -notmatch "^[Ss]$") {
    Write-Host "Operacion cancelada por el usuario" -ForegroundColor Yellow
    exit 0
}

try {
    Write-Host "Eliminando tarea existente (si existe)..." -ForegroundColor Yellow
    & schtasks /delete /tn $TaskName /f 2>$null

    Write-Host "Creando nueva tarea programada..." -ForegroundColor Yellow
    
    # Crear la tarea usando schtasks
    $result = & schtasks /create `
        /tn $TaskName `
        /tr "`"$ExecuteScript`"" `
        /sc minute `
        /mo $Interval `
        /st "00:00" `
        /et "23:59" `
        /du "23:59" `
        /ri $Interval `
        /f `
        /rl highest `
        /ru "SYSTEM" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=================================================================" -ForegroundColor Green
        Write-Host "TAREA CREADA EXITOSAMENTE" -ForegroundColor Green
        Write-Host "=================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Detalles de la tarea:" -ForegroundColor Cyan
        Write-Host "  Nombre: $TaskName"
        Write-Host "  Frecuencia: Cada $Interval minutos"
        Write-Host "  Ejecucion: 24/7 (bot valida horario internamente)"
        Write-Host "  Usuario: SYSTEM (privilegios elevados)"
        Write-Host ""
        Write-Host "Caracteristicas del bot:" -ForegroundColor Cyan
        Write-Host "  Solo procesa en horario laboral (8am-5pm)"
        Write-Host "  Solo dias habiles de Colombia (Lun-Vie)"
        Write-Host "  Excluye festivos colombianos"
        Write-Host "  Logs organizados por fecha en logs/DDMMAAAA/"
        Write-Host ""
        Write-Host "Comandos utiles:" -ForegroundColor Yellow
        Write-Host "  Ver estado:    schtasks /query /tn `"$TaskName`""
        Write-Host "  Ejecutar ahora: schtasks /run /tn `"$TaskName`""
        Write-Host "  Deshabilitar:  schtasks /change /tn `"$TaskName`" /disable"
        Write-Host "  Habilitar:     schtasks /change /tn `"$TaskName`" /enable"
        Write-Host "  Eliminar:      schtasks /delete /tn `"$TaskName`" /f"
        Write-Host ""

        # Verificar estado
        Write-Host "Verificando estado de la tarea..." -ForegroundColor Yellow
        & schtasks /query /tn $TaskName /fo table

        # Opcion de ejecutar inmediatamente
        Write-Host ""
        $runNow = Read-Host "Deseas ejecutar la tarea ahora para probar? (S/N)"
        if ($runNow -match "^[Ss]$") {
            Write-Host "Ejecutando tarea..." -ForegroundColor Yellow
            & schtasks /run /tn $TaskName
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Tarea ejecutada correctamente. Revisa los logs para ver el resultado." -ForegroundColor Green
            } else {
                Write-Host "Hubo un problema al ejecutar la tarea" -ForegroundColor Yellow
            }
        }

    } else {
        throw "Error al crear la tarea. Codigo de salida: $LASTEXITCODE"
    }

} catch {
    Write-Host ""
    Write-Host "ERROR: No se pudo crear la tarea" -ForegroundColor Red
    Write-Host "Detalles del error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Salida del comando:" -ForegroundColor Cyan
    Write-Host $result
    Write-Host ""
    Write-Host "Posibles soluciones:" -ForegroundColor Cyan
    Write-Host "1. Verificar que se ejecuta como Administrador"
    Write-Host "2. Comprobar que el servicio Task Scheduler esta ejecutandose"
    Write-Host "3. Verificar permisos del usuario actual"
    Write-Host "4. Usar el script .bat alternativo: crear_tarea_windows.bat"
}

Write-Host ""
Read-Host "Presiona Enter para salir"
