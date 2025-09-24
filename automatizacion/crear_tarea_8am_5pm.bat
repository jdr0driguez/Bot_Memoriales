@echo off
REM ===================================================================
REM Script para crear tarea que ejecuta el bucle infinito de 8am a 5pm
REM El bucle infinito se inicia a las 8am y se detiene a las 5pm
REM ===================================================================

SETLOCAL ENABLEDELAYEDEXPANSION

:: Configuracion de la tarea
SET TASK_NAME=BotMemorialesBucleInfinito
SET SCRIPT_PATH=%~dp0..\ejecutar_mejorado.bat
SET TASK_STOP_NAME=BotMemorialesDetener

:: Obtener ruta absoluta del script
FOR %%i IN ("%SCRIPT_PATH%") DO SET SCRIPT_PATH_ABS=%%~fi

echo ===================================================================
echo CREANDO TAREA PARA BUCLE INFINITO 8AM-5PM
echo ===================================================================
echo.
echo Nombre de la tarea: %TASK_NAME%
echo Script a ejecutar: %SCRIPT_PATH_ABS%
echo Horario: 8:00 AM a 5:00 PM (Lunes a Viernes)
echo Logica: Bucle infinito controlado por horario
echo.

:: Verificar si el script existe
IF NOT EXIST "%SCRIPT_PATH_ABS%" (
    echo ERROR: No se encuentra el script ejecutar_mejorado.bat
    echo Ruta buscada: %SCRIPT_PATH_ABS%
    pause
    exit /b 1
)

:: Eliminar tareas existentes si existen
echo Eliminando tareas existentes (si existen)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
schtasks /delete /tn "%TASK_STOP_NAME%" /f >nul 2>&1

:: Crear tarea para INICIAR a las 8:00 AM (Lunes a Viernes)
echo Creando tarea de INICIO (8:00 AM)...
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"%SCRIPT_PATH_ABS%\"" ^
    /sc weekly ^
    /d MON,TUE,WED,THU,FRI ^
    /st 08:00 ^
    /f ^
    /rl highest

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo crear la tarea de inicio
    pause
    exit /b 1
)

:: Crear tarea para DETENER a las 5:00 PM (Lunes a Viernes)
echo Creando tarea de DETENCION (5:00 PM)...
schtasks /create ^
    /tn "%TASK_STOP_NAME%" ^
    /tr "taskkill /f /im cmd.exe /fi \"WINDOWTITLE eq Administrador: C:\WINDOWS\system32\cmd.exe*\"" ^
    /sc weekly ^
    /d MON,TUE,WED,THU,FRI ^
    /st 17:00 ^
    /f ^
    /rl highest

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo crear la tarea de detencion
    pause
    exit /b 1
)

echo.
echo ===================================================================
echo TAREAS CREADAS EXITOSAMENTE
echo ===================================================================
echo.
echo TAREA DE INICIO:
echo   Nombre: %TASK_NAME%
echo   Horario: 8:00 AM (Lunes a Viernes)
echo   Accion: Inicia el bucle infinito
echo.
echo TAREA DE DETENCION:
echo   Nombre: %TASK_STOP_NAME%
echo   Horario: 5:00 PM (Lunes a Viernes)
echo   Accion: Detiene todos los procesos cmd.exe del bot
echo.
echo IMPORTANTE:
echo - El bot ejecutara su bucle infinito de 8am a 5pm
echo - Solo en dias habiles (Lun-Vie)
echo - El bot internamente valida festivos colombianos
echo - Los logs se guardan en logs/DDMMAAAA/
echo.
echo Comandos utiles:
echo   Ver tareas:     schtasks /query /tn "%TASK_NAME%"
echo   Ejecutar ahora: schtasks /run /tn "%TASK_NAME%"
echo   Detener ahora:  schtasks /run /tn "%TASK_STOP_NAME%"
echo   Eliminar todo:  schtasks /delete /tn "%TASK_NAME%" /f ^&^& schtasks /delete /tn "%TASK_STOP_NAME%" /f
echo.

echo Presiona cualquier tecla para continuar...
pause >nul
