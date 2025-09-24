@echo off
REM ===================================================================
REM Script para crear tarea automática en Windows Task Scheduler
REM Ejecuta el bot cada 5 minutos, todos los días
REM El bot internamente valida si debe ejecutarse (horario laboral)
REM ===================================================================

SETLOCAL ENABLEDELAYEDEXPANSION

:: Configuración de la tarea
SET TASK_NAME=BotMemorialesAutomatico
SET SCRIPT_PATH=%~dp0..\ejecutar_mejorado.bat
SET LOG_PATH=%~dp0..\logs\task_scheduler.log

:: Obtener ruta absoluta del script
FOR %%i IN ("%SCRIPT_PATH%") DO SET SCRIPT_PATH_ABS=%%~fi

echo ===================================================================
echo CREANDO TAREA AUTOMATICA EN WINDOWS TASK SCHEDULER
echo ===================================================================
echo.
echo Nombre de la tarea: %TASK_NAME%
echo Script a ejecutar: %SCRIPT_PATH_ABS%
echo Frecuencia: Cada 5 minutos, todos los días
echo Horario: El bot valida internamente el horario laboral
echo.

:: Verificar si el script existe
IF NOT EXIST "%SCRIPT_PATH_ABS%" (
    echo ERROR: No se encuentra el script ejecutar_mejorado.bat
    echo Ruta buscada: %SCRIPT_PATH_ABS%
    echo.
    echo Asegurate de ejecutar este script desde la carpeta automatizacion/
    pause
    exit /b 1
)

:: Eliminar tarea existente si existe
echo Eliminando tarea existente (si existe)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: Crear nueva tarea
echo Creando nueva tarea programada...
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"%SCRIPT_PATH_ABS%\"" ^
    /sc minute ^
    /mo 5 ^
    /st 00:00 ^
    /et 23:59 ^
    /du 23:59 ^
    /ri 5 ^
    /f ^
    /rl highest

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================================================
    echo TAREA CREADA EXITOSAMENTE
    echo ===================================================================
    echo.
    echo La tarea "%TASK_NAME%" ha sido creada y configurada para:
    echo - Ejecutarse cada 5 minutos
    echo - Funcionar 24/7 (el bot valida horario internamente)
    echo - Ejecutarse con privilegios elevados
    echo.
    echo IMPORTANTE:
    echo - El bot solo procesará expedientes en horario laboral (8am-5pm)
    echo - Solo en días hábiles de Colombia (Lun-Vie, excluyendo festivos)
    echo - Los logs se guardan en: logs/DDMMAAAA/
    echo.
    echo Para administrar la tarea:
    echo - Ver estado: schtasks /query /tn "%TASK_NAME%"
    echo - Ejecutar ahora: schtasks /run /tn "%TASK_NAME%"
    echo - Deshabilitar: schtasks /change /tn "%TASK_NAME%" /disable
    echo - Habilitar: schtasks /change /tn "%TASK_NAME%" /enable
    echo - Eliminar: schtasks /delete /tn "%TASK_NAME%" /f
    echo.
    echo La tarea se puede administrar también desde:
    echo Inicio ^> Administrador de tareas ^> Biblioteca del Programador de tareas
    echo.
) ELSE (
    echo.
    echo ERROR: No se pudo crear la tarea programada
    echo Código de error: %ERRORLEVEL%
    echo.
    echo Posibles soluciones:
    echo 1. Ejecutar como Administrador
    echo 2. Verificar permisos del usuario
    echo 3. Comprobar que el Servicio Programador de tareas esté ejecutándose
    echo.
)

echo Presiona cualquier tecla para continuar...
pause >nul
