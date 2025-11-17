# Docker Deployment Guide

## Quick Start

The easiest way to run Mac Health Pulse in Docker:

```bash
./docker-run.sh start
```

Connect via VNC to `localhost:5900` (password: `healthpulse`)

## Commands

```bash
./docker-run.sh start      # Start the application
./docker-run.sh stop       # Stop the application
./docker-run.sh restart    # Restart the application
./docker-run.sh logs       # View logs
./docker-run.sh build      # Rebuild Docker image
./docker-run.sh clean      # Remove containers and images
```

## Manual Docker Commands

If you prefer docker-compose directly:

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose build --no-cache
```

## Connecting to the Application

### macOS
1. Open **Finder**
2. Press `Cmd + K`
3. Enter: `vnc://localhost:5900`
4. Password: `healthpulse`

Or use the built-in Screen Sharing app.

### Windows
1. Install [TightVNC Viewer](https://www.tightvnc.com/) or [RealVNC](https://www.realvnc.com/)
2. Connect to: `localhost:5900`
3. Password: `healthpulse`

### Linux
```bash
# Using Remmina (GUI)
remmina -c vnc://localhost:5900

# Using vncviewer (CLI)
vncviewer localhost:5900
```

## Configuration

### Change VNC Password

Edit `docker-compose.yml`:

```yaml
environment:
  - VNC_PASSWORD=your_secure_password
```

### Change Resolution

Edit `docker-compose.yml`:

```yaml
environment:
  - RESOLUTION=1920x1080x24  # WIDTHxHEIGHTxDEPTH
```

## Important Limitations

### Current Docker Setup (VNC-based)

⚠️ **The containerized version has limitations:**

1. **System Monitoring**: Shows container metrics, NOT host system metrics
2. **macOS Features**: AppleScript and launchctl are not available in Linux containers
3. **Startup Management**: Cannot manage host system startup items
4. **Performance**: VNC adds network latency

### What Works in Docker

✅ UI/UX demonstration
✅ Application interface testing
✅ Container-level process monitoring
✅ Code development and testing

### What Doesn't Work

❌ Real macOS system monitoring
❌ Managing macOS startup items
❌ AppleScript execution
❌ launchctl daemon management

## For Production Use

For real system monitoring, you need the **native macOS version**:

```bash
# Run natively on macOS
./run.sh
```

Or see `SCALING.md` for web-based architecture that supports cross-platform monitoring.

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 5900
lsof -i :5900

# Kill the process or change the port in docker-compose.yml
ports:
  - "5901:5900"  # Use 5901 instead
```

### Application Not Starting

```bash
# View logs
./docker-run.sh logs

# Check specific service logs
docker-compose logs app
docker-compose logs x11vnc
```

### Can't Connect via VNC

1. Ensure container is running: `docker ps`
2. Check logs: `./docker-run.sh logs`
3. Verify port mapping: `docker port mac-health-pulse`
4. Try different VNC client

## Next Steps

- See `SCALING.md` for production deployment strategies
- See `OPENSOURCE.md` for contribution guidelines
- See `ARCHITECTURE.md` for web-based refactor plans
