#!/bin/bash

# Hawaiian LeniLani Chatbot Deployment Script
# Deploy with Aloha! 🌺

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="hawaiian-lenilani-chatbot"
COMPOSE_FILE="docker-compose.hawaiian.yml"
ENV_FILE=".env.production"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# ASCII Art
print_header() {
    echo -e "${GREEN}"
    cat << "EOF"
    _  _                   _ _              _            _ _            _ 
   | || |__ ___ __ ____ _(_|_)__ _ _ _    | |   ___ _ _(_) |__ _ _ _ (_)
   | __ / _` \ V  V / _` | | / _` | ' \   | |__/ -_) ' \ | / _` | ' \| |
   |_||_\__,_|\_/\_/\__,_|_|_\__,_|_||_|  |____\___|_||_|_|_\__,_|_||_|_|
                                                                          
                    🌺 AI Consulting Chatbot Deployment 🌺
EOF
    echo -e "${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed!"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed!"
        exit 1
    fi
    
    # Check environment file
    if [ ! -f "$ENV_FILE" ]; then
        error "Environment file $ENV_FILE not found!"
        exit 1
    fi
    
    # Check compose file
    if [ ! -f "$COMPOSE_FILE" ]; then
        error "Docker Compose file $COMPOSE_FILE not found!"
        exit 1
    fi
    
    log "Prerequisites check passed ✓"
}

# Validate environment
validate_environment() {
    log "Validating environment configuration..."
    
    # Check required environment variables
    required_vars=(
        "POSTGRES_PASSWORD"
        "REDIS_PASSWORD"
        "ANTHROPIC_API_KEY"
        "SECRET_KEY"
        "JWT_SECRET_KEY"
    )
    
    source "$ENV_FILE"
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            error "Required environment variable $var is not set!"
            exit 1
        fi
    done
    
    log "Environment validation passed ✓"
}

# Build images
build_images() {
    log "Building Docker images..."
    
    docker-compose -f "$COMPOSE_FILE" build --parallel
    
    log "Docker images built successfully ✓"
}

# Deploy services
deploy_services() {
    log "Deploying services..."
    
    # Stop existing services
    info "Stopping existing services..."
    docker-compose -f "$COMPOSE_FILE" down
    
    # Start services
    info "Starting services..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # Wait for services to be healthy
    info "Waiting for services to be healthy..."
    sleep 10
    
    # Check service health
    services=("postgres" "redis" "rasa" "rasa-actions" "backend" "frontend" "nginx")
    
    for service in "${services[@]}"; do
        if docker-compose -f "$COMPOSE_FILE" ps | grep -q "${PROJECT_NAME}_${service}.*Up"; then
            log "Service $service is running ✓"
        else
            error "Service $service is not running!"
            docker-compose -f "$COMPOSE_FILE" logs "$service" | tail -20
        fi
    done
}

# Run migrations
run_migrations() {
    log "Running database migrations..."
    
    # Wait for PostgreSQL to be ready
    info "Waiting for PostgreSQL to be ready..."
    docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U lenilani -d hawaiian_lenilani
    
    # Initialize database if needed
    if ! docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U lenilani -d hawaiian_lenilani -c "SELECT 1 FROM chatbot.conversations LIMIT 1;" &> /dev/null; then
        info "Initializing database..."
        docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U lenilani -d hawaiian_lenilani < init-db.sql
        log "Database initialized ✓"
    else
        log "Database already initialized ✓"
    fi
}

# Train Rasa model
train_rasa_model() {
    log "Training Rasa model..."
    
    docker-compose -f "$COMPOSE_FILE" exec -T rasa rasa train
    
    log "Rasa model trained successfully ✓"
}

# Health check
health_check() {
    log "Running health checks..."
    
    # Check API health
    if curl -s -f http://localhost/health > /dev/null; then
        log "API health check passed ✓"
    else
        error "API health check failed!"
    fi
    
    # Check frontend
    if curl -s -f http://localhost > /dev/null; then
        log "Frontend health check passed ✓"
    else
        error "Frontend health check failed!"
    fi
    
    # Check Rasa
    if curl -s -f http://localhost:5005/status > /dev/null; then
        log "Rasa health check passed ✓"
    else
        warning "Rasa health check failed - this might be normal during initial startup"
    fi
}

# Show deployment info
show_deployment_info() {
    echo
    info "🎉 Deployment completed successfully! 🎉"
    echo
    info "Access your Hawaiian LeniLani Chatbot at:"
    echo "   🌐 https://hawaii.lenilani.com"
    echo
    info "Service URLs:"
    echo "   📊 API: https://hawaii.lenilani.com/api"
    echo "   💬 WebSocket: wss://hawaii.lenilani.com/ws"
    echo "   🤖 Rasa: http://localhost:5005"
    echo
    info "Monitoring:"
    echo "   📈 Metrics: http://localhost:9090/metrics"
    echo "   🏥 Health: https://hawaii.lenilani.com/health"
    echo
    info "Commands:"
    echo "   View logs: docker-compose -f $COMPOSE_FILE logs -f"
    echo "   Stop services: docker-compose -f $COMPOSE_FILE down"
    echo "   Restart services: docker-compose -f $COMPOSE_FILE restart"
    echo
    log "Mahalo for deploying with us! 🌺"
}

# Main deployment flow
main() {
    print_header
    
    # Parse arguments
    case "${1:-deploy}" in
        deploy)
            check_prerequisites
            validate_environment
            build_images
            deploy_services
            run_migrations
            train_rasa_model
            health_check
            show_deployment_info
            ;;
        build)
            check_prerequisites
            build_images
            ;;
        start)
            check_prerequisites
            docker-compose -f "$COMPOSE_FILE" up -d
            ;;
        stop)
            docker-compose -f "$COMPOSE_FILE" down
            ;;
        restart)
            docker-compose -f "$COMPOSE_FILE" restart
            ;;
        logs)
            docker-compose -f "$COMPOSE_FILE" logs -f "${2:-}"
            ;;
        status)
            docker-compose -f "$COMPOSE_FILE" ps
            ;;
        backup)
            docker-compose -f "$COMPOSE_FILE" exec backup /scripts/backup-postgres.sh
            docker-compose -f "$COMPOSE_FILE" exec backup /scripts/backup-redis.sh
            ;;
        *)
            error "Unknown command: $1"
            echo "Usage: $0 [deploy|build|start|stop|restart|logs|status|backup]"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"