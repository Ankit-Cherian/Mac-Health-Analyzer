#!/bin/bash

# Mac Health Pulse - Simple Docker Runner
# This script makes it easy to run the dockerized application

set -e

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================"
echo "Mac Health Pulse - Docker Launcher"
echo -e "======================================${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}docker-compose is not installed. Please install docker-compose first.${NC}"
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "Usage: ./docker-run.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the application (default)"
    echo "  stop        Stop the application"
    echo "  restart     Restart the application"
    echo "  logs        View application logs"
    echo "  build       Rebuild the Docker image"
    echo "  clean       Stop and remove containers and images"
    echo ""
}

# Parse command
COMMAND=${1:-start}

case "$COMMAND" in
    start)
        echo -e "${GREEN}Starting Mac Health Pulse...${NC}\n"
        docker-compose up -d
        echo -e "\n${GREEN}✓ Application started!${NC}"
        echo -e "${BLUE}======================================"
        echo "Connect to the application:"
        echo "  VNC: localhost:5900"
        echo "  Password: healthpulse"
        echo ""
        echo "Recommended VNC clients:"
        echo "  - macOS: Built-in Screen Sharing"
        echo "  - Windows: TightVNC, RealVNC"
        echo "  - Linux: Remmina, TigerVNC"
        echo ""
        echo "To view logs: ./docker-run.sh logs"
        echo -e "======================================${NC}"
        ;;

    stop)
        echo -e "${YELLOW}Stopping Mac Health Pulse...${NC}"
        docker-compose down
        echo -e "${GREEN}✓ Application stopped${NC}"
        ;;

    restart)
        echo -e "${YELLOW}Restarting Mac Health Pulse...${NC}"
        docker-compose restart
        echo -e "${GREEN}✓ Application restarted${NC}"
        ;;

    logs)
        echo -e "${BLUE}Showing logs (Ctrl+C to exit)...${NC}\n"
        docker-compose logs -f
        ;;

    build)
        echo -e "${YELLOW}Rebuilding Docker image...${NC}"
        docker-compose build --no-cache
        echo -e "${GREEN}✓ Build complete${NC}"
        ;;

    clean)
        echo -e "${YELLOW}Cleaning up containers and images...${NC}"
        docker-compose down --rmi all --volumes
        echo -e "${GREEN}✓ Cleanup complete${NC}"
        ;;

    help|--help|-h)
        show_usage
        ;;

    *)
        echo -e "${YELLOW}Unknown command: $COMMAND${NC}\n"
        show_usage
        exit 1
        ;;
esac
