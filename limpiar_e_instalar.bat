@echo off
echo [INFO] Limpiando e instalando dependencias...

:: Eliminar entorno virtual anterior si existe
IF EXIST vScrap (
    echo [INFO] Eliminando entorno virtual anterior...
    rmdir /s vScrap
)

IF EXIST vScrap_clean (
    echo [INFO] Eliminando entorno virtual limpio anterior...
    rmdir /s vScrap_clean
)

:: Crear nuevo entorno virtual
echo [INFO] Creando nuevo entorno virtual...
python -m venv vScrap_clean

:: Activar entorno virtual
echo [INFO] Activando entorno virtual...
call vScrap_clean\Scripts\activate.bat

:: Instalar dependencias
echo [INFO] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo [INFO] Instalación completada exitosamente!
echo [INFO] Ahora puedes ejecutar ejecutar_mejorado.bat
pause 