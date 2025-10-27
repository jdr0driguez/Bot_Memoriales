# ✅ Checklist Pre-Docker

## Antes de construir el contenedor Docker

### 📋 Verificaciones Obligatorias

- [ ] **Docker instalado y funcionando**
  ```cmd
  docker --version
  docker-compose --version
  ```
  - Docker: versión 20.10 o superior
  - Docker Compose: versión 1.29 o superior

- [ ] **Archivo `config.py` con credenciales correctas**
  - HOST (servidor SSH/SFTP)
  - USERNAME y PASSWORD
  - KEYHASH para desencriptación

- [ ] **Archivo `cases.json` presente en el directorio raíz**

- [ ] **Todas las dependencias listadas en `pyproject.toml`**
  - ✅ Ya está configurado con todas las dependencias de `requirements.txt`

### 📁 Estructura de Archivos

Verifica que tengas estos archivos:

```
Bot_MemorialesFinal - copia (3)/
├── Dockerfile                    # ✅ Creado
├── docker-compose.yml            # ✅ Creado
├── .dockerignore                 # ✅ Creado
├── pyproject.toml               # ✅ Creado
├── docker-run.bat               # ✅ Creado (Windows)
├── docker-run.sh                # ✅ Creado (Linux/Mac)
├── config.py                    # ⚠️  Verificar credenciales
├── cases.json                   # ⚠️  Debe existir
├── main.py                      # ✅ Existente
├── logger.py                    # ✅ Existente
├── core/                        # ✅ Existente
│   ├── API_Consumo.py
│   ├── API_Modelos.py
│   ├── API_parser.py
│   ├── db_Connection.py
│   ├── email_service.py
│   └── ...
└── logs/                        # 📂 Se creará automáticamente
```

### 🔐 Seguridad

- [ ] **No subir credenciales a Git**
  - El archivo `.gitignore` está configurado para ignorar `.env`
  - ⚠️ **IMPORTANTE**: `config.py` NO está en .gitignore (contiene credenciales hardcoded)
  - **Recomendación**: Migrar a variables de entorno en el futuro

### 🐧 Solo Linux/Mac

Si estás en Linux o Mac, dale permisos de ejecución al script:

```bash
chmod +x docker-run.sh
```

---

## 🚀 Prueba Inicial

### Paso 1: Build
```cmd
docker-run.bat build              # Windows
./docker-run.sh build            # Linux/Mac
```

**Tiempo estimado**: 5-10 minutos (primera vez)

### Paso 2: Prueba una ejecución única
```cmd
docker-run.bat run-once           # Windows
./docker-run.sh run-once         # Linux/Mac
```

### Paso 3: Verificar logs
```cmd
# Verificar que se hayan creado los logs
dir logs                          # Windows
ls -la logs                      # Linux/Mac
```

---

## ✅ Todo Listo

Si todos los pasos anteriores fueron exitosos:

```cmd
# Iniciar en modo continuo (background)
docker-run.bat start              # Windows
./docker-run.sh start            # Linux/Mac

# Ver logs en tiempo real
docker-run.bat logs               # Windows
./docker-run.sh logs             # Linux/Mac
```

---

## 🆘 Troubleshooting

### Error: "Cannot connect to Docker daemon"
- **Windows**: Inicia Docker Desktop
- **Linux**: `sudo systemctl start docker`

### Error: "No such file or directory: cases.json"
- Asegúrate de que `cases.json` esté en el directorio raíz

### Error: "Access denied" en logs/
- **Windows**: Docker Desktop necesita permisos en la carpeta
- **Linux**: `chmod 777 logs/`

### Error: "ODBC Driver not found"
- El Dockerfile ya incluye la instalación de Microsoft ODBC Driver 18
- Si persiste, verifica la conexión a la base de datos en `config.py`

### Build muy lento
- Primera construcción: normal (descarga imágenes base)
- Construcciones posteriores: usa caché (más rápido)
- Para forzar rebuild completo: `docker-run.bat update`

---

## 📊 Monitoreo

### Ver uso de recursos
```cmd
docker-run.bat stats              # Windows
./docker-run.sh stats            # Linux/Mac
```

### Ver estado del contenedor
```cmd
docker-run.bat status             # Windows
./docker-run.sh status           # Linux/Mac
```

---

## ✅ Verificación Final

Después de iniciar el bot, verifica:

- [ ] Contenedor corriendo: `docker-run.bat status`
- [ ] Logs generándose: `docker-run.bat logs`
- [ ] Archivos en `logs/` accesibles desde el host
- [ ] Bot procesando elementos correctamente

---

**¡Felicitaciones! Tu bot está dockerizado y listo para producción** 🎉

