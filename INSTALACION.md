# Instalación del Bot de Memoriales

## Requisitos Previos

1. **Python 3.8 o superior**
   - Descargar desde: https://python.org
   - Asegurarse de marcar "Add Python to PATH" durante la instalación

2. **Acceso a Internet**
   - Para descargar las dependencias

## Instalación Automática (Recomendada)

### Paso 1: Descargar el proyecto
```bash
# Clonar o descargar el proyecto en tu máquina
# Asegúrate de estar en la carpeta raíz del proyecto
```

### Paso 2: Ejecutar el instalador
```bash
# En Windows, ejecutar:
instalar_dependencias.bat

# O hacer doble clic en el archivo instalar_dependencias.bat
```

### Paso 3: Verificar la instalación
El instalador verificará automáticamente:
- ✅ Python instalado
- ✅ Entorno virtual creado
- ✅ Dependencias instaladas
- ✅ Módulos críticos funcionando

## Instalación Manual

Si el instalador automático falla, puedes instalar manualmente:

### Paso 1: Crear entorno virtual
```bash
python -m venv vScrap_clean
```

### Paso 2: Activar entorno virtual
```bash
# En Windows:
vScrap_clean\Scripts\activate.bat

# En Linux/Mac:
source vScrap_clean/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Verificar instalación
```bash
python -c "import requests; print('requests OK')"
python -c "import selenium; print('selenium OK')"
python -c "import psycopg2; print('psycopg2 OK')"
```

## Ejecución

Una vez instalado, ejecutar el bot:

```bash
# En Windows:
ejecutar_mejorado.bat

# O hacer doble clic en ejecutar_mejorado.bat
```

## Solución de Problemas

### Error: "No module named 'requests'"
**Solución:**
1. Ejecutar `instalar_dependencias.bat`
2. O manualmente: `pip install requests==2.32.4`

### Error: "No module named 'selenium'"
**Solución:**
1. Ejecutar `instalar_dependencias.bat`
2. O manualmente: `pip install selenium==4.34.2`

### Error: Entorno virtual no se activa
**Solución:**
1. Eliminar carpeta `vScrap_clean`
2. Ejecutar `instalar_dependencias.bat`

### Error: Python no encontrado
**Solución:**
1. Instalar Python desde https://python.org
2. Marcar "Add Python to PATH" durante instalación
3. Reiniciar la terminal/CMD

## Estructura de Archivos

```
Bot_MemorialesFinal/
├── instalar_dependencias.bat    # Instalador automático
├── ejecutar_mejorado.bat        # Script de ejecución
├── requirements.txt             # Lista de dependencias
├── main.py                     # Archivo principal
├── core/                       # Módulos del bot
├── logs/                       # Archivos de log
└── vScrap_clean/              # Entorno virtual (se crea)
```

## Dependencias Principales

- **requests**: Para llamadas HTTP
- **selenium**: Para automatización web
- **psycopg2**: Para conexión a PostgreSQL
- **paramiko**: Para conexiones SFTP
- **python-dotenv**: Para variables de entorno
- **pillow**: Para procesamiento de imágenes
- **opencv-python**: Para procesamiento de imágenes
- **pycryptodome**: Para encriptación

## Contacto

Si tienes problemas con la instalación, verifica:
1. Python está instalado y en el PATH
2. Tienes acceso a Internet
3. Ejecutas los scripts como administrador si es necesario 