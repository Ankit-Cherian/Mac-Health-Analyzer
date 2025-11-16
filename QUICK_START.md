# Quick Start Guide

## Installation

1. **Install Python dependencies**:
```bash
pip3 install -r requirements.txt
```

2. **Run the application**:
```bash
python3 main.py
```

Or make it executable and run directly:
```bash
chmod +x main.py
./main.py
```

## Features

### ⚡ Startup Items Tab
- View all login items, Launch Agents, and Launch Daemons
- See which items are enabled or disabled
- Search and filter by type
- Disable unwanted startup items
- Color-coded status indicators

### 📊 Running Processes Tab
- Real-time process monitoring
- Sortable by memory, CPU, or name
- Search for specific processes
- Force quit unresponsive applications
- Toggle system process visibility
- Memory and CPU usage metrics

### 🖥️ System Overview Tab
- Total system memory
- CPU core count
- Active process count
- Startup items summary
- Top resource consumers

## Tips

- **Startup Items**: Be careful when disabling system-critical items. If unsure, leave it enabled.
- **Force Quit**: Always try to quit applications normally before force quitting.
- **Refresh**: Data auto-refreshes every 2-3 seconds, or click Refresh manually.
- **Search**: Use the search bar to quickly find specific items or processes.
- **Sorting**: Click column headers to sort by that column.

## Permissions

Some operations may require administrator privileges:
- Disabling Launch Daemons
- Killing system processes
- Accessing system-level startup items

Run with `sudo` if you need elevated privileges:
```bash
sudo python3 main.py
```

## Troubleshooting

### Fonts not loading
The app will automatically download Bricolage Grotesque and JetBrains Mono fonts from Google Fonts on first run. If this fails:
- Check your internet connection
- The app will fall back to system fonts

### "Permission Denied" errors
Some system operations require administrator privileges. Run with `sudo` or use System Preferences to manage those items.

### Process list is empty
Make sure to enable "Include System Processes" if you want to see all processes.

## Keyboard Shortcuts

- **⌘Q**: Quit application
- **⌘R**: Refresh current tab
- **⌘F**: Focus search bar (when available)

## Uninstallation

Simply delete the application folder. No system files are modified.

## Support

For issues or questions, check the README.md file.

