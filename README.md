# Mac Health Analyzer

A macOS system monitoring and startup management tool with a modern interface.

## Features

- View and manage startup items (login items, launch agents, launch daemons)
- Monitor running processes with real-time CPU and memory usage
- Force quit unresponsive applications
- System overview with resource metrics
- Search and filter functionality

## Requirements

- macOS 10.14 or later
- Python 3.9+

## Installation

Clone the repository:

```bash
git clone https://github.com/Ankit-Cherian/mac-health-analyzer.git
cd mac-health-analyzer
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

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

## Interface

The application provides three main tabs:

- **Startup Items** - View and disable items that launch at startup
- **Running Processes** - Monitor active processes and resource usage
- **System Overview** - View overall system health metrics

## Notes

- Custom fonts (Bricolage Grotesque, JetBrains Mono) will download automatically on first run
- Some operations require administrator privileges
- The application auto-refreshes active tab every 10 seconds
- Process table displays up to 100 processes for optimal performance

## Built With

- PyQt6 - GUI framework
- psutil - System and process utilities
- Python 3.9+
