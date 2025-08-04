@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Configuración del script
SET BASE_DIR=%~dp0
SET VENV_DIR=vScrap_clean
SET INTERVALO_MINUTOS=5
SET CONTADOR_CICLOS=0
SET ARCHIVO_LOG=logs\ejecucion_automatizacion.log

:: Crear directorio de logs si no existe
IF NOT EXIST logs mkdir logs

:: Cambiar al directorio base
cd /d %BASE_DIR%

:: Log de inicio
echo [%date% %time%] Iniciando automatización en bucle infinito
echo [%date% %time%] Iniciando automatización en bucle infinito >> %ARCHIVO_LOG%
echo [%date% %time%] Directorio base: %BASE_DIR%
echo [%date% %time%] Directorio base: %BASE_DIR% >> %ARCHIVO_LOG%
echo [%date% %time%] Intervalo de ejecución: %INTERVALO_MINUTOS% minutos
echo [%date% %time%] Intervalo de ejecución: %INTERVALO_MINUTOS% minutos >> %ARCHIVO_LOG%

:: Crear entorno virtual si no existe
IF NOT EXIST %VENV_DIR% (
    echo [%date% %time%] Creando entorno virtual...
    echo [%date% %time%] Creando entorno virtual... >> %ARCHIVO_LOG%
    python -m venv %VENV_DIR%
    IF %ERRORLEVEL% NEQ 0 (
        echo [%date% %time%] ERROR: No se pudo crear el entorno virtual
        echo [%date% %time%] ERROR: No se pudo crear el entorno virtual >> %ARCHIVO_LOG%
        pause
        exit /b 1
    )
)

:: Activar entorno virtual
echo [%date% %time%] Activando entorno virtual...
echo [%date% %time%] Activando entorno virtual... >> %ARCHIVO_LOG%
call %VENV_DIR%\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: No se pudo activar el entorno virtual
    echo [%date% %time%] ERROR: No se pudo activar el entorno virtual >> %ARCHIVO_LOG%
    pause
    exit /b 1
)

:: Verificar que el entorno esté activado correctamente
echo [%date% %time%] Verificando entorno virtual activado...
echo [%date% %time%] Verificando entorno virtual activado... >> %ARCHIVO_LOG%
python -c "import sys; print('Entorno virtual:', sys.prefix)" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: El entorno virtual no está activado correctamente
    echo [%date% %time%] ERROR: El entorno virtual no está activado correctamente >> %ARCHIVO_LOG%
    pause
    exit /b 1
)

:: Instalar/actualizar dependencias
echo [%date% %time%] Verificando dependencias...
echo [%date% %time%] Verificando dependencias... >> %ARCHIVO_LOG%

:: Verificar dependencias críticas
python -c "import requests" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: requests no está instalado
    echo [%date% %time%] ERROR: requests no está instalado >> %ARCHIVO_LOG%
    echo [%date% %time%] Ejecuta instalar_dependencias.bat para instalar las dependencias
    echo [%date% %time%] Ejecuta instalar_dependencias.bat para instalar las dependencias >> %ARCHIVO_LOG%
    pause
    exit /b 1
)

python -c "import selenium" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: selenium no está instalado
    echo [%date% %time%] ERROR: selenium no está instalado >> %ARCHIVO_LOG%
    echo [%date% %time%] Ejecuta instalar_dependencias.bat para instalar las dependencias
    echo [%date% %time%] Ejecuta instalar_dependencias.bat para instalar las dependencias >> %ARCHIVO_LOG%
    pause
    exit /b 1
)

:: Actualizar dependencias si es necesario
pip install --upgrade pip --quiet >nul 2>&1
pip install -r requirements.txt --quiet >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] WARNING: Algunas dependencias no se pudieron actualizar
    echo [%date% %time%] WARNING: Algunas dependencias no se pudieron actualizar >> %ARCHIVO_LOG%
)

echo [%date% %time%] Configuración completada. Iniciando bucle de ejecución...
echo [%date% %time%] Configuración completada. Iniciando bucle de ejecución... >> %ARCHIVO_LOG%
echo [%date% %time%] Presiona Ctrl+C para detener el proceso
echo [%date% %time%] Presiona Ctrl+C para detener el proceso >> %ARCHIVO_LOG%
echo.

:BUCLE_PRINCIPAL
SET /A CONTADOR_CICLOS+=1

echo.
echo ========================================
echo [CICLO %CONTADOR_CICLOS%] %date% %time%
echo ========================================
echo [%date% %time%] Iniciando ciclo %CONTADOR_CICLOS%
echo [%date% %time%] Iniciando ciclo %CONTADOR_CICLOS% >> %ARCHIVO_LOG%

:: Ejecutar el proceso principal
echo [%date% %time%] Ejecutando automatización...
echo [%date% %time%] Ejecutando automatización... >> %ARCHIVO_LOG%
python -W ignore::DeprecationWarning main.py
SET CODIGO_SALIDA=%ERRORLEVEL%

:: Evaluar resultado de la ejecución
IF %CODIGO_SALIDA% EQU 0 (
    echo [%date% %time%] Ciclo %CONTADOR_CICLOS% completado exitosamente
    echo [%date% %time%] Ciclo %CONTADOR_CICLOS% completado exitosamente >> %ARCHIVO_LOG%
) ELSE IF %CODIGO_SALIDA% EQU 1 (
    echo [%date% %time%] Ciclo %CONTADOR_CICLOS% completado sin expedientes para procesar
    echo [%date% %time%] Ciclo %CONTADOR_CICLOS% completado sin expedientes para procesar >> %ARCHIVO_LOG%
) ELSE (
    echo [%date% %time%] WARNING: Ciclo %CONTADOR_CICLOS% completado con errores (código: %CODIGO_SALIDA%)
    echo [%date% %time%] WARNING: Ciclo %CONTADOR_CICLOS% completado con errores (código: %CODIGO_SALIDA%) >> %ARCHIVO_LOG%
)

:: Calcular tiempo de espera
echo [%date% %time%] Esperando %INTERVALO_MINUTOS% minutos antes del siguiente ciclo...
echo [%date% %time%] Esperando %INTERVALO_MINUTOS% minutos antes del siguiente ciclo... >> %ARCHIVO_LOG%
echo [%date% %time%] Volverá a ejecutar en %INTERVALO_MINUTOS% minutos...
echo [%date% %time%] Volverá a ejecutar en %INTERVALO_MINUTOS% minutos... >> %ARCHIVO_LOG%

:: Esperar silenciosamente (convertir minutos a segundos)
SET /A SEGUNDOS_ESPERA=%INTERVALO_MINUTOS% * 60
timeout /t !SEGUNDOS_ESPERA! /nobreak >nul

echo [%date% %time%] Tiempo de espera completado. Iniciando siguiente ciclo...
echo [%date% %time%] Tiempo de espera completado. Iniciando siguiente ciclo... >> %ARCHIVO_LOG%
goto BUCLE_PRINCIPAL 