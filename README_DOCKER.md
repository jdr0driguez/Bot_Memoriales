# 🐳 Guía de Docker para Bot de Memoriales

## 📋 Requisitos Previos

- Docker instalado (versión 20.10+)
- Docker Compose instalado (versión 1.29+)
- Al menos 2GB de RAM disponible
- Espacio en disco: ~500MB

## 🚀 Inicio Rápido

### 1. Construir la imagen

```bash
docker-compose build
```

### 2. Ejecutar el bot

```bash
docker-compose up
```

Para ejecutar en segundo plano (detached mode):

```bash
docker-compose up -d
```

### 3. Ver logs en tiempo real

```bash
docker-compose logs -f bot-memoriales
```

### 4. Detener el bot

```bash
docker-compose down
```

## 📂 Acceso a Logs

Los logs se almacenan en la carpeta `./logs` del host y son accesibles directamente:

```
Bot_MemorialesFinal/
├── logs/                    # ← Logs accesibles desde el host
│   ├── 27102025/           # Logs por fecha
│   │   ├── debug.log
│   │   ├── info.log
│   │   ├── error.log
│   │   └── ...
│   ├── debug.log           # Logs principales
│   └── ...
```

### Ver logs desde el host

```bash
# Ver logs del día actual
cat logs/$(date +%d%m%Y)/info.log

# Ver logs en tiempo real
tail -f logs/info.log

# Buscar errores
grep -r "ERROR" logs/
```

## 🔧 Configuración

### Modificar configuración sin rebuild

Si necesitas cambiar `config.py` sin reconstruir la imagen, descomenta la línea en `docker-compose.yml`:

```yaml
volumes:
  - ./logs:/app/logs:rw
  - ./config.py:/app/config.py:ro  # ← Descomenta esta línea
```

Luego reinicia el contenedor:

```bash
docker-compose restart
```

### Usar variables de entorno (.env)

Para mayor seguridad, puedes migrar las credenciales de `config.py` a un archivo `.env`:

1. Copia `.env.example` como `.env`
2. Completa los valores reales
3. Modifica `config.py` para leer desde variables de entorno

## 📊 Monitoreo

### Ver estado del contenedor

```bash
docker-compose ps
```

### Ver uso de recursos

```bash
docker stats bot-memoriales
```

### Inspeccionar el contenedor

```bash
docker inspect bot-memoriales
```

## 🔄 Actualización

Cuando realices cambios en el código:

```bash
# Detener el contenedor
docker-compose down

# Reconstruir la imagen
docker-compose build

# Iniciar nuevamente
docker-compose up -d
```

## 🐛 Troubleshooting

### El bot no inicia

```bash
# Ver logs completos
docker-compose logs bot-memoriales

# Verificar configuración
docker-compose config
```

### Problemas con permisos de logs

```bash
# En Linux/Mac, asegurar permisos correctos
chmod 777 logs/
```

### Limpiar todo y empezar de cero

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes (¡CUIDADO! Borra los logs)
docker-compose down -v

# Eliminar imagen
docker rmi bot-memoriales:latest

# Reconstruir
docker-compose build
docker-compose up -d
```

## 🕐 Ejecución Programada (Cron)

### Opción 1: Cron del host (Linux/Mac)

```bash
# Editar crontab
crontab -e

# Ejecutar cada 30 minutos
*/30 * * * * cd /ruta/al/proyecto && docker-compose run --rm bot-memoriales
```

### Opción 2: Scheduler con Ofelia (Recomendado)

Descomenta la sección de `bot-scheduler` en `docker-compose.yml` y ajusta el horario:

```yaml
labels:
  ofelia.job-run.bot-memoriales.schedule: "@every 30m"  # Cada 30 minutos
```

Luego:

```bash
docker-compose up -d
```

### Opción 3: Tarea Programada de Windows

Crea un script `ejecutar_docker.bat`:

```batch
@echo off
cd /d "C:\ruta\al\proyecto"
docker-compose run --rm bot-memoriales
```

Programa la tarea en el Programador de Tareas de Windows.

## 🏗️ Arquitectura del Dockerfile

```
┌─────────────────────────────────────┐
│  STAGE 1: BUILDER                   │
│  - Instala dependencias de sistema  │
│  - Compila paquetes Python          │
│  - Crea virtualenv                  │
└────────────┬────────────────────────┘
             │
             │ Copia solo el virtualenv
             ↓
┌─────────────────────────────────────┐
│  STAGE 2: RUNNER (Imagen final)     │
│  - Solo runtime dependencies        │
│  - Usuario sin privilegios (botuser)│
│  - Imagen optimizada (~300MB)       │
└─────────────────────────────────────┘
```

## 🔒 Buenas Prácticas Implementadas

✅ Construcción en dos fases (builder/runner)  
✅ Usuario sin privilegios (`botuser`)  
✅ Volúmenes para logs persistentes  
✅ Variables de entorno seguras  
✅ Healthchecks configurados  
✅ Límites de recursos definidos  
✅ Logging estructurado  
✅ .dockerignore optimizado  

## 📞 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.

