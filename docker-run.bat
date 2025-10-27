@echo off
REM ============================================================================
REM Script de utilidades para Bot de Memoriales Docker (Windows)
REM ============================================================================

setlocal enabledelayedexpansion

if "%~1"=="" goto :help

set COMMAND=%~1

if /i "%COMMAND%"=="build" goto :build
if /i "%COMMAND%"=="start" goto :start
if /i "%COMMAND%"=="run" goto :run
if /i "%COMMAND%"=="stop" goto :stop
if /i "%COMMAND%"=="restart" goto :restart
if /i "%COMMAND%"=="logs" goto :logs
if /i "%COMMAND%"=="status" goto :status
if /i "%COMMAND%"=="stats" goto :stats
if /i "%COMMAND%"=="shell" goto :shell
if /i "%COMMAND%"=="clean" goto :clean
if /i "%COMMAND%"=="view-logs" goto :view_logs
if /i "%COMMAND%"=="run-once" goto :run_once
if /i "%COMMAND%"=="update" goto :update
if /i "%COMMAND%"=="help" goto :help

echo [ERROR] Comando desconocido: %COMMAND%
echo.
goto :help

:build
echo [INFO] Construyendo imagen Docker...
docker-compose build
if %errorlevel% equ 0 (
    echo [SUCCESS] Imagen construida exitosamente
) else (
    echo [ERROR] Error al construir la imagen
    exit /b 1
)
goto :end

:start
echo [INFO] Iniciando bot en modo detached...
docker-compose up -d
if %errorlevel% equ 0 (
    echo [SUCCESS] Bot iniciado. Usa 'docker-run.bat logs' para ver la salida
) else (
    echo [ERROR] Error al iniciar el bot
    exit /b 1
)
goto :end

:run
echo [INFO] Ejecutando bot en modo interactivo...
docker-compose up
goto :end

:stop
echo [INFO] Deteniendo bot...
docker-compose down
if %errorlevel% equ 0 (
    echo [SUCCESS] Bot detenido
) else (
    echo [ERROR] Error al detener el bot
    exit /b 1
)
goto :end

:restart
echo [INFO] Reiniciando bot...
docker-compose restart
if %errorlevel% equ 0 (
    echo [SUCCESS] Bot reiniciado
) else (
    echo [ERROR] Error al reiniciar el bot
    exit /b 1
)
goto :end

:logs
echo [INFO] Mostrando logs en tiempo real (Ctrl+C para salir)...
docker-compose logs -f bot-memoriales
goto :end

:status
echo [INFO] Estado del contenedor:
docker-compose ps
goto :end

:stats
echo [INFO] Estadisticas de uso de recursos:
docker stats bot-memoriales --no-stream
goto :end

:shell
echo [INFO] Abriendo shell en el contenedor...
docker-compose exec bot-memoriales /bin/bash
goto :end

:clean
echo [WARNING] Esta accion eliminara contenedores, imagenes y volumenes
set /p CONFIRM="Estas seguro? (S/N): "
if /i "!CONFIRM!"=="S" (
    echo [INFO] Limpiando recursos Docker...
    docker-compose down -v
    docker rmi bot-memoriales:latest 2>nul
    echo [SUCCESS] Limpieza completada
) else (
    echo [INFO] Operacion cancelada
)
goto :end

:view_logs
set LOG_DIR=.\logs
if exist "%LOG_DIR%" (
    echo [INFO] Logs disponibles en %LOG_DIR%:
    dir /b "%LOG_DIR%"
    echo.
    echo [INFO] Ver log especifico:
    echo   - Info:  type %LOG_DIR%\info.log
    echo   - Error: type %LOG_DIR%\error.log
    echo   - Debug: type %LOG_DIR%\debug.log
) else (
    echo [WARNING] No se encontro el directorio de logs
)
goto :end

:run_once
echo [INFO] Ejecutando bot una sola vez...
docker-compose run --rm bot-memoriales
if %errorlevel% equ 0 (
    echo [SUCCESS] Ejecucion completada
) else (
    echo [ERROR] Error en la ejecucion
    exit /b 1
)
goto :end

:update
echo [INFO] Actualizando bot (rebuild)...
docker-compose down
docker-compose build --no-cache
docker-compose up -d
if %errorlevel% equ 0 (
    echo [SUCCESS] Bot actualizado y reiniciado
) else (
    echo [ERROR] Error al actualizar
    exit /b 1
)
goto :end

:help
echo ============================================================================
echo   Bot de Memoriales - Utilidades Docker (Windows)
echo ============================================================================
echo.
echo Uso: docker-run.bat ^<comando^>
echo.
echo Comandos disponibles:
echo.
echo   build       - Construir la imagen Docker
echo   start       - Iniciar el bot en segundo plano
echo   run         - Ejecutar el bot en modo interactivo
echo   stop        - Detener el bot
echo   restart     - Reiniciar el bot
echo   logs        - Ver logs en tiempo real
echo   status      - Ver estado del contenedor
echo   stats       - Ver uso de recursos
echo   shell       - Acceder al shell del contenedor
echo   view-logs   - Ver ubicacion de logs del host
echo   run-once    - Ejecutar bot una sola vez
echo   update      - Reconstruir y reiniciar (para actualizaciones)
echo   clean       - Limpiar todo (contenedores, imagenes, volumenes)
echo   help        - Mostrar esta ayuda
echo.
echo Ejemplos:
echo   docker-run.bat build
echo   docker-run.bat start
echo   docker-run.bat logs
echo   docker-run.bat run-once
echo.
goto :end

:end
endlocal
exit /b 0

