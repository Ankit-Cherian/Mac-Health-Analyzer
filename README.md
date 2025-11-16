# Mac Health Analyzer Dashboard

A powerful, visually stunning macOS system monitoring and startup management tool with a distinctive UI.

## Features

- 🚀 **Startup Items Management**: View and control all login items, Launch Agents, and Launch Daemons
- 📊 **Real-time Process Monitoring**: Track CPU and memory usage of all running processes
- 🎨 **Beautiful UI**: Modern glassmorphic design with custom typography (Bricolage Grotesque & JetBrains Mono)
- ⚡ **Performance Focused**: Lightweight and efficient, won't slow down your Mac
- 🔍 **Easy Management**: Force quit apps, disable startup items, and optimize your system

## Installation

### Prerequisites

- macOS 10.14 or later
- Python 3.9 or higher

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

3. Run the application:

```bash
python3 main.py
```

## Usage

### Startup Items Tab

- View all applications and services that launch at startup
- Toggle items on/off to optimize boot time
- See the location and type of each startup item

### Running Processes Tab

- Monitor all active processes in real-time
- Sort by CPU usage, memory consumption, or process name
- Force quit unresponsive applications
- Filter to show only user applications or include system processes

### System Overview Tab

- View overall system health metrics
- See top resource-consuming processes at a glance
- Monitor total RAM and CPU usage

## Permissions

The app may request permissions to:

- Read system information
- Manage startup items
- Terminate processes

These permissions are used solely for the functionality of the app and your data never leaves your Mac.

## Troubleshooting

### "Permission Denied" Errors

Some system-level operations may require administrator privileges. Run with sudo if needed:

```bash
sudo python3 main.py
```

### Fonts Not Loading

The app will automatically download required fonts on first run. If this fails, check your internet connection and try again.

## Technical Details

Built with:

- **PyQt6**: Modern GUI framework
- **psutil**: System and process utilities
- **AppleScript**: macOS system integration
- **launchctl**: Startup item management

## License

For personal use. Built with ❤️ for Mac power users.
