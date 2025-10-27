# 🚀 Inicio Rápido - Docker

## ⚡ En 3 Pasos

### 1️⃣ Construir la imagen

**Windows:**
```cmd
docker-run.bat build
```

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh build
```

### 2️⃣ Iniciar el bot

**Windows:**
```cmd
docker-run.bat start
```

**Linux/Mac:**
```bash
./docker-run.sh start
```

### 3️⃣ Ver los logs

**Windows:**
```cmd
docker-run.bat logs
```

**Linux/Mac:**
```bash
./docker-run.sh logs
```

---

## 📂 ¿Dónde están los logs?

Los logs están en la carpeta `logs` del proyecto y son accesibles directamente:

```
Bot_MemorialesFinal - copia (3)/
├── logs/                    # ← Aquí están tus logs
│   ├── 27102025/           # Logs del día de hoy
│   │   ├── debug.log
│   │   ├── info.log
│   │   ├── error.log
│   │   └── warning.log
│   ├── debug.log           # Log principal
│   └── info.log
```

Puedes abrir estos archivos con cualquier editor de texto mientras el contenedor está corriendo.

---

## 🛠️ Comandos Útiles

### Detener el bot
```cmd
docker-run.bat stop          # Windows
./docker-run.sh stop         # Linux/Mac
```

### Reiniciar el bot
```cmd
docker-run.bat restart       # Windows
./docker-run.sh restart      # Linux/Mac
```

### Ver estado
```cmd
docker-run.bat status        # Windows
./docker-run.sh status       # Linux/Mac
```

### Ejecutar una sola vez (sin dejarlo corriendo)
```cmd
docker-run.bat run-once      # Windows
./docker-run.sh run-once     # Linux/Mac
```

### Ver todos los comandos disponibles
```cmd
docker-run.bat help          # Windows
./docker-run.sh help         # Linux/Mac
```

---

## 🔄 Actualizar después de cambios en el código

Cuando modifiques archivos de Python:

**Windows:**
```cmd
docker-run.bat update
```

**Linux/Mac:**
```bash
./docker-run.sh update
```

---

## ❓ Problemas Comunes

### "Docker no está instalado"
- Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop

### "Permisos denegados" (Linux)
```bash
sudo usermod -aG docker $USER
# Luego cierra sesión e inicia nuevamente
```

### "El bot no inicia"
Revisa los logs:
```cmd
docker-run.bat logs
```

---

## 📖 Documentación Completa

Para información más detallada, consulta:
- **README_DOCKER.md** - Guía completa de Docker
- **README.md** - Documentación general del proyecto

