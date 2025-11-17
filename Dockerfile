# Mac Health Pulse - Docker VNC Image
# This creates a containerized version with VNC access

FROM ubuntu:22.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    x11vnc \
    xvfb \
    fluxbox \
    wget \
    wmctrl \
    supervisor \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install PyQt6 system dependencies
RUN apt-get update && apt-get install -y \
    libegl1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libgl1-mesa-glx \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY *.py .
COPY ui/ ./ui/
COPY utils/ ./utils/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Create VNC directory
RUN mkdir -p ~/.vnc

# Setup supervisord config
RUN mkdir -p /var/log/supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose VNC port
EXPOSE 5900
EXPOSE 6080

# Set display environment variable
ENV DISPLAY=:1
ENV RESOLUTION=1920x1080x24

# Create entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
