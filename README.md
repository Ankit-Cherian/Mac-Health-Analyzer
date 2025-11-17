# Mac Health Analyzer - Neon Terminal Edition

A stunning macOS system monitoring and startup management tool with a **cyberpunk-inspired interface**, real-time visualizations, and advanced analytics.

![Version](https://img.shields.io/badge/version-2.0-neon)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Platform](https://img.shields.io/badge/platform-macOS-blue)

## ✨ Features

### 🎨 Stunning Neon UI
- **Cyberpunk Terminal Aesthetic** - Unique neon green, electric cyan, and hot pink color scheme
- **Custom Typography** - Chakra Petch, Rajdhani, Orbitron, and JetBrains Mono fonts
- **Glassmorphic Panels** - Modern card-based design with transparency effects
- **Smooth Animations** - Buttery 60fps animations and transitions

### 📊 Real-Time Visualizations
- **Live CPU & Memory Graphs** - Real-time line charts showing system resource usage
- **Circular Gauges** - Beautiful animated gauges for at-a-glance metrics
- **Bar Charts** - Top resource consumers displayed with neon-styled horizontal bars
- **Sparklines** - Mini charts for inline metrics (coming soon)

### ⚡ System Monitoring
- **Startup Items Management** - View and disable items that launch at startup
  - Login items
  - Launch agents
  - Launch daemons
  - Quick toggle switches with smooth animations

- **Process Monitoring** - Monitor active processes with detailed metrics
  - Real-time CPU and memory usage
  - Search and filter processes
  - Force quit unresponsive applications
  - Color-coded status indicators

- **System Overview Dashboard** - Comprehensive system health at a glance
  - Real-time CPU usage monitoring with trend charts
  - Memory usage tracking with visual gauges
  - Process count and system information
  - Top resource consumers with interactive bar charts

## 🖼️ Screenshots

The interface features:
- **Dark cyberpunk theme** with neon accents
- **3 enhanced tabs**: ⚡ STARTUP, ⚙ PROCESSES, ◉ SYSTEM
- **Real-time charts** updating every 2 seconds
- **Circular gauges** with color-coded status
- **Horizontal bar charts** showing top processes

## 🚀 Requirements

- **macOS** 10.14 or later
- **Python** 3.9+
- **Screen resolution**: 1280x800 minimum (optimized for Retina displays)

## 📦 Installation

### Option 1: Native macOS (Recommended)

Clone the repository:

```bash
git clone https://github.com/Ankit-Cherian/mac-health-analyzer.git
cd mac-health-analyzer
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Dependencies include:
- `PyQt6` - Modern GUI framework
- `psutil` - System and process utilities
- `pyqtgraph` - High-performance scientific graphics
- `numpy` - Numerical computing for charts

### Option 2: Docker (Cross-Platform)

**Quick Start:**
```bash
./docker-run.sh start
```

Connect via VNC to `localhost:5900` (password: `healthpulse`)

See [DOCKER.md](DOCKER.md) for detailed Docker setup instructions.

## 💻 Usage

### Native macOS

Run the application:

```bash
python3 main.py
```

Or use the launch script:

```bash
./run.sh
```

For system-level access (viewing launch daemons, managing system processes):

```bash
sudo python3 main.py
```

### Docker

```bash
# Start the application
./docker-run.sh start

# View logs
./docker-run.sh logs

# Stop the application
./docker-run.sh stop
```

See [DOCKER.md](DOCKER.md) for VNC client setup and troubleshooting.

## 🎯 Interface Guide

### ⚡ STARTUP Tab
- View all startup items in a searchable table
- Filter by type (Login Items, Launch Agents, Launch Daemons)
- Toggle items on/off with smooth animated switches
- Search functionality for quick filtering

### ⚙ PROCESSES Tab
- Monitor all running processes
- View CPU and memory usage in real-time
- Search processes by name
- Filter system processes
- Force quit processes with one click
- Color-coded resource usage (green = low, amber = medium, pink = high)

### ◉ SYSTEM Tab (NEW!)
- **Circular Gauges** - CPU, Memory, and Process count with animated needles
- **Real-Time Charts** - Live graphs showing CPU and memory trends over the last 60 data points
- **Resource Bar Charts** - Top 8 processes by CPU and memory usage
- **System Information Cards** - Total RAM, CPU cores, startup items count
- **Status Indicator** - Online/error status in the top right

## 🎨 Design System

### Color Palette
- **Primary**: Neon Green `#00ff41` - Matrix-inspired accent
- **Secondary**: Electric Cyan `#00f5ff` - Futuristic highlights
- **Tertiary**: Hot Pink `#ff006e` - Critical alerts
- **Warning**: Amber `#ffbe0b` - Medium priority
- **Background**: Deep Black `#0a0a0f` - Terminal darkness

### Typography
- **Display Font**: Chakra Petch (Thai-inspired geometric)
- **Secondary**: Rajdhani (Indo-Arabic inspired)
- **Special**: Orbitron (Futuristic headers)
- **Monospace**: JetBrains Mono (Code and metrics)

### Charts & Visualizations
- **Real-time Line Charts** - Smooth 60-point scrolling graphs with neon glow
- **Circular Gauges** - 360° animated gauges with gradient fills
- **Horizontal Bar Charts** - Gradient-filled bars with percentage display
- **Color Coding**:
  - 0-50% = Neon Green (optimal)
  - 50-80% = Amber (warning)
  - 80-100% = Hot Pink (critical)

## ⚙️ Performance

- **Chart Update Rate**: 2 seconds (configurable)
- **Process Limit**: 100 processes displayed for optimal performance
- **Animation Frame Rate**: 60 FPS
- **Memory Efficient**: Charts use rolling buffers with 60-point maximum

## 🔧 Advanced Configuration

The application automatically:
- Downloads custom fonts on first run
- Caches launchctl results for faster startup
- Uses signal blocking during updates to prevent UI freezing
- Refreshes only the active tab to conserve resources

## 📝 Notes

- Custom fonts (Chakra Petch, Rajdhani, Orbitron, JetBrains Mono) download automatically on first run
- Some operations require administrator privileges
- Charts update every 2 seconds when System tab is active
- Process table displays up to 100 processes for optimal performance
- All visualizations use hardware acceleration when available

## 🛠️ Built With

- **PyQt6** - Modern cross-platform GUI framework
- **PyQtGraph** - Scientific graphics and GUI library for real-time visualization
- **psutil** - Cross-platform library for system and process monitoring
- **NumPy** - Fundamental package for numerical computing
- **Python 3.9+** - Programming language

## 🐳 Docker & Deployment

Mac Health Pulse can be deployed in multiple ways:

1. **Native macOS** - Best for personal use and full feature access
2. **Docker (VNC)** - Cross-platform demo and development
3. **Web-based** - Scalable, multi-user architecture (in development)

### Documentation

- **[DOCKER.md](DOCKER.md)** - Docker setup and VNC access
- **[SCALING.md](SCALING.md)** - Production deployment and scaling strategies
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Web-based refactor technical design

### Quick Docker Deployment

```bash
# One-command start
./docker-run.sh start

# Access via VNC: localhost:5900
```

## 🎯 Future Enhancements

### Near-term
- [ ] Export system reports to PDF/CSV
- [ ] Custom alert thresholds
- [ ] Historical data tracking and trends
- [ ] Network monitoring tab
- [ ] Disk usage visualization

### Long-term (Web Version)
- [ ] Cross-platform support (Linux, Windows)
- [ ] Web-based interface
- [ ] Multi-user support
- [ ] REST API for integrations
- [ ] Mobile app (React Native)
- [ ] Cloud deployment options

See [SCALING.md](SCALING.md) for the complete roadmap.

## 📄 License

This project is part of the mac-health-analyzer repository.

## 🙏 Acknowledgments

- Inspired by cyberpunk and terminal aesthetics
- Font families from Google Fonts and JetBrains
- Icons and symbols from Unicode character set
- PyQtGraph for exceptional visualization capabilities

---

**Made with neon dreams and terminal vibes** ✨
