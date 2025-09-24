@echo off
REM ===================================================================
REM Script para gestionar la tarea automática del Bot de Memoriales
REM Permite ver estado, ejecutar, habilitar, deshabilitar y eliminar
REM ===================================================================

SETLOCAL ENABLEDELAYEDEXPANSION

SET TASK_NAME=BotMemorialesAutomatico

:MENU
cls
echo ===================================================================
echo GESTION DE TAREA AUTOMATICA - BOT DE MEMORIALES
echo ===================================================================
echo.
echo Tarea: %TASK_NAME%
echo.
echo Opciones disponibles:
echo.
echo 1. Ver estado de la tarea
echo 2. Ejecutar tarea ahora (una vez)
echo 3. Habilitar tarea automática
echo 4. Deshabilitar tarea automática
echo 5. Ver información detallada
echo 6. Ver logs recientes
echo 7. Eliminar tarea completamente
echo 8. Crear/Recrear tarea
echo 9. Salir
echo.
set /p OPCION=Selecciona una opción (1-9): 

IF "%OPCION%"=="1" goto VER_ESTADO
IF "%OPCION%"=="2" goto EJECUTAR_AHORA
IF "%OPCION%"=="3" goto HABILITAR
IF "%OPCION%"=="4" goto DESHABILITAR
IF "%OPCION%"=="5" goto INFO_DETALLADA
IF "%OPCION%"=="6" goto VER_LOGS
IF "%OPCION%"=="7" goto ELIMINAR
IF "%OPCION%"=="8" goto CREAR_TAREA
IF "%OPCION%"=="9" goto SALIR

echo Opción inválida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:VER_ESTADO
echo.
echo ===================================================================
echo ESTADO DE LA TAREA
echo ===================================================================
schtasks /query /tn "%TASK_NAME%" /fo table /v
echo.
pause
goto MENU

:EJECUTAR_AHORA
echo.
echo Ejecutando tarea ahora...
schtasks /run /tn "%TASK_NAME%"
IF %ERRORLEVEL% EQU 0 (
    echo Tarea ejecutada exitosamente.
) ELSE (
    echo Error al ejecutar la tarea.
)
echo.
pause
goto MENU

:HABILITAR
echo.
echo Habilitando tarea automática...
schtasks /change /tn "%TASK_NAME%" /enable
IF %ERRORLEVEL% EQU 0 (
    echo Tarea habilitada exitosamente.
) ELSE (
    echo Error al habilitar la tarea.
)
echo.
pause
goto MENU

:DESHABILITAR
echo.
echo Deshabilitando tarea automática...
schtasks /change /tn "%TASK_NAME%" /disable
IF %ERRORLEVEL% EQU 0 (
    echo Tarea deshabilitada exitosamente.
) ELSE (
    echo Error al deshabilitar la tarea.
)
echo.
pause
goto MENU

:INFO_DETALLADA
echo.
echo ===================================================================
echo INFORMACIÓN DETALLADA DE LA TAREA
echo ===================================================================
schtasks /query /tn "%TASK_NAME%" /fo list /v
echo.
pause
goto MENU

:VER_LOGS
echo.
echo ===================================================================
echo LOGS RECIENTES
echo ===================================================================
echo.
echo Logs de ejecución automática:
IF EXIST "..\logs\ejecucion_automatizacion.log" (
    echo Últimas 20 líneas:
    powershell "Get-Content '..\logs\ejecucion_automatizacion.log' -Tail 20"
) ELSE (
    echo No se encontró el archivo de logs de ejecución.
)
echo.
echo Logs del bot (carpeta de hoy):
FOR /f "tokens=1-3 delims=/" %%a IN ('date /t') DO (
    SET DIA=%%a
    SET MES=%%b  
    SET ANO=%%c
)
SET FECHA_HOY=%DIA%%MES%%ANO%
IF EXIST "..\logs\%FECHA_HOY%\WS_RNEC.log" (
    echo Últimas 10 líneas del log principal:
    powershell "Get-Content '..\logs\%FECHA_HOY%\WS_RNEC.log' -Tail 10"
) ELSE (
    echo No se encontraron logs del bot para hoy.
)
echo.
pause
goto MENU

:ELIMINAR
echo.
echo ===================================================================
echo ELIMINAR TAREA
echo ===================================================================
echo.
echo ADVERTENCIA: Esto eliminará completamente la tarea automática.
echo El bot dejará de ejecutarse automáticamente.
echo.
set /p CONFIRMAR=¿Estás seguro? (S/N): 
IF /I "%CONFIRMAR%"=="S" (
    schtasks /delete /tn "%TASK_NAME%" /f
    IF %ERRORLEVEL% EQU 0 (
        echo Tarea eliminada exitosamente.
    ) ELSE (
        echo Error al eliminar la tarea.
    )
) ELSE (
    echo Operación cancelada.
)
echo.
pause
goto MENU

:CREAR_TAREA
echo.
echo Ejecutando script de creación de tarea...
call crear_tarea_windows.bat
pause
goto MENU

:SALIR
echo.
echo Saliendo...
exit /b 0
