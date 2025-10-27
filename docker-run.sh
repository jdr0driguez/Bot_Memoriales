#!/bin/bash
# ============================================================================
# Script de utilidades para Bot de Memoriales Docker
# ============================================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones auxiliares
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función: Construir imagen
build() {
    print_info "Construyendo imagen Docker..."
    docker-compose build
    print_success "Imagen construida exitosamente"
}

# Función: Iniciar bot
start() {
    print_info "Iniciando bot en modo detached..."
    docker-compose up -d
    print_success "Bot iniciado. Usa './docker-run.sh logs' para ver la salida"
}

# Función: Iniciar bot en foreground
run() {
    print_info "Ejecutando bot en modo interactivo..."
    docker-compose up
}

# Función: Detener bot
stop() {
    print_info "Deteniendo bot..."
    docker-compose down
    print_success "Bot detenido"
}

# Función: Reiniciar bot
restart() {
    print_info "Reiniciando bot..."
    docker-compose restart
    print_success "Bot reiniciado"
}

# Función: Ver logs
logs() {
    print_info "Mostrando logs en tiempo real (Ctrl+C para salir)..."
    docker-compose logs -f bot-memoriales
}

# Función: Ver estado
status() {
    print_info "Estado del contenedor:"
    docker-compose ps
}

# Función: Ver estadísticas de recursos
stats() {
    print_info "Estadísticas de uso de recursos:"
    docker stats bot-memoriales --no-stream
}

# Función: Acceder al shell del contenedor
shell() {
    print_info "Abriendo shell en el contenedor..."
    docker-compose exec bot-memoriales /bin/bash
}

# Función: Limpiar todo
clean() {
    print_warning "Esta acción eliminará contenedores, imágenes y volúmenes"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Limpiando recursos Docker..."
        docker-compose down -v
        docker rmi bot-memoriales:latest 2>/dev/null || true
        print_success "Limpieza completada"
    else
        print_info "Operación cancelada"
    fi
}

# Función: Ver logs de archivo del host
view_logs() {
    LOG_DIR="./logs"
    if [ -d "$LOG_DIR" ]; then
        print_info "Logs disponibles en $LOG_DIR:"
        ls -lh "$LOG_DIR"
        echo ""
        print_info "Ver log específico:"
        echo "  - Info:  tail -f $LOG_DIR/info.log"
        echo "  - Error: tail -f $LOG_DIR/error.log"
        echo "  - Debug: tail -f $LOG_DIR/debug.log"
    else
        print_warning "No se encontró el directorio de logs"
    fi
}

# Función: Ejecutar una sola vez
run_once() {
    print_info "Ejecutando bot una sola vez..."
    docker-compose run --rm bot-memoriales
    print_success "Ejecución completada"
}

# Función: Actualizar (rebuild)
update() {
    print_info "Actualizando bot (rebuild)..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    print_success "Bot actualizado y reiniciado"
}

# Menú de ayuda
help() {
    echo "============================================================================"
    echo "  Bot de Memoriales - Utilidades Docker"
    echo "============================================================================"
    echo ""
    echo "Uso: ./docker-run.sh <comando>"
    echo ""
    echo "Comandos disponibles:"
    echo ""
    echo "  build       - Construir la imagen Docker"
    echo "  start       - Iniciar el bot en segundo plano"
    echo "  run         - Ejecutar el bot en modo interactivo"
    echo "  stop        - Detener el bot"
    echo "  restart     - Reiniciar el bot"
    echo "  logs        - Ver logs en tiempo real"
    echo "  status      - Ver estado del contenedor"
    echo "  stats       - Ver uso de recursos"
    echo "  shell       - Acceder al shell del contenedor"
    echo "  view-logs   - Ver ubicación de logs del host"
    echo "  run-once    - Ejecutar bot una sola vez"
    echo "  update      - Reconstruir y reiniciar (para actualizaciones)"
    echo "  clean       - Limpiar todo (contenedores, imágenes, volúmenes)"
    echo "  help        - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./docker-run.sh build && ./docker-run.sh start"
    echo "  ./docker-run.sh logs"
    echo "  ./docker-run.sh run-once"
    echo ""
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    help
    exit 0
fi

# Ejecutar comando
case "$1" in
    build)
        build
        ;;
    start)
        start
        ;;
    run)
        run
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    stats)
        stats
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    view-logs)
        view_logs
        ;;
    run-once)
        run_once
        ;;
    update)
        update
        ;;
    help)
        help
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo ""
        help
        exit 1
        ;;
esac

