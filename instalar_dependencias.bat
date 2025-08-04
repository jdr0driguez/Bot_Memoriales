@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo ========================================
echo INSTALADOR DE DEPENDENCIAS - BOT MEMORIALES
echo ========================================
echo.

:: Configuración
SET BASE_DIR=%~dp0
SET VENV_DIR=vScrap_clean
SET REQUIREMENTS_FILE=requirements.txt

:: Cambiar al directorio base
cd /d %BASE_DIR%

echo [INFO] Directorio base: %BASE_DIR%
echo [INFO] Verificando Python...

:: Verificar que Python esté instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo [ERROR] Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

python --version
echo.

:: Eliminar entorno virtual anterior si existe
IF EXIST %VENV_DIR% (
    echo [INFO] Eliminando entorno virtual anterior...
    rmdir /s /q %VENV_DIR%
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] No se pudo eliminar el entorno virtual anterior
        pause
        exit /b 1
    )
)

:: Crear nuevo entorno virtual
echo [INFO] Creando nuevo entorno virtual...
python -m venv %VENV_DIR%
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)

:: Activar entorno virtual
echo [INFO] Activando entorno virtual...
call %VENV_DIR%\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

:: Verificar que el entorno esté activado
echo [INFO] Verificando activación del entorno...
python -c "import sys; print('Entorno virtual activado:', sys.prefix)" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] El entorno virtual no se activó correctamente
    pause
    exit /b 1
)

:: Mostrar información del entorno activado
echo [INFO] Verificando que pip esté usando el entorno virtual...
python -c "import sys; print('Python ejecutándose desde:', sys.executable)" 2>nul
pip --version 2>nul
echo [INFO] Todas las dependencias se instalarán en el entorno virtual

:: Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip --quiet
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] No se pudo actualizar pip, continuando...
)

:: Verificar que requirements.txt existe
IF NOT EXIST %REQUIREMENTS_FILE% (
    echo [ERROR] No se encontró el archivo %REQUIREMENTS_FILE%
    pause
    exit /b 1
)

:: Instalar dependencias
echo [INFO] Instalando dependencias desde %REQUIREMENTS_FILE%...
echo [INFO] Esto puede tomar varios minutos...

pip install -r %REQUIREMENTS_FILE% --quiet
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Error al instalar dependencias
    echo [INFO] Intentando instalar dependencias una por una...
    
    :: Instalar dependencias críticas una por una
    echo [INFO] Instalando requests...
    pip install requests==2.32.4 --quiet
    echo [INFO] Instalando selenium...
    pip install selenium==4.34.2 --quiet
    echo [INFO] Instalando psycopg2-binary...
    pip install psycopg2-binary --quiet
    echo [INFO] Instalando paramiko...
    pip install paramiko==3.4.0 --quiet
    echo [INFO] Instalando python-dotenv...
    pip install python-dotenv==1.1.1 --quiet
    echo [INFO] Instalando pillow...
    pip install pillow==11.3.0 --quiet
    echo [INFO] Instalando opencv-python...
    pip install opencv-python==4.12.0.88 --quiet
    echo [INFO] Instalando numpy...
    pip install numpy==2.2.6 --quiet
    echo [INFO] Instalando pycryptodome...
    pip install pycryptodome==3.19.1 --quiet
    echo [INFO] Instalando pyodbc...
    pip install pyodbc==5.1.0 --quiet
)

:: Verificar instalación de dependencias críticas
echo [INFO] Verificando instalación de dependencias críticas...

python -c "import requests; print('✓ requests instalado')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] requests no se instaló correctamente
    pause
    exit /b 1
)

python -c "import selenium; print('✓ selenium instalado')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] selenium no se instaló correctamente
    pause
    exit /b 1
)

python -c "import psycopg2; print('✓ psycopg2 instalado')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] psycopg2 no se instaló correctamente
)

python -c "import paramiko; print('✓ paramiko instalado')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] paramiko no se instaló correctamente
)

:: Crear directorio de logs si no existe
IF NOT EXIST logs mkdir logs

echo.
echo ========================================
echo INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo [INFO] Entorno virtual: %VENV_DIR%
echo [INFO] Para ejecutar el bot usa: ejecutar_mejorado.bat
echo [INFO] Para limpiar e instalar de nuevo usa: limpiar_e_instalar.bat
echo.
echo [INFO] Presiona cualquier tecla para salir...
pause >nul 