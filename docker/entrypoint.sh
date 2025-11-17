#!/bin/bash
set -e

# Set default VNC password if not provided
export VNC_PASSWORD=${VNC_PASSWORD:-healthpulse}

# Set default resolution if not provided
export RESOLUTION=${RESOLUTION:-1920x1080x24}

echo "======================================"
echo "Mac Health Pulse - Docker Container"
echo "======================================"
echo "VNC Server starting on port 5900"
echo "Resolution: $RESOLUTION"
echo "VNC Password: $VNC_PASSWORD"
echo "======================================"
echo "Connect using VNC client to: localhost:5900"
echo "======================================"

# Execute the CMD
exec "$@"
