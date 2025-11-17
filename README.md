# Mac Health Analyzer

A simple macOS app I built to see what's running on my Mac and manage startup items.

## Screenshots

### Onboarding

<img src="docs/screenshots/start up step 1.png" width="700">

*First-time setup guide explaining what the app does*

<img src="docs/screenshots/startupsetup4.png" width="700">

*Helpful tips for using the app safely*

### Main Interface

**Startup Tab** - Manage what launches when you boot up

<img src="docs/screenshots/MainStartupPage.png" width="700">

*View all your startup items with stats on enabled/disabled items*

**Processes Tab** - Monitor what's running

<img src="docs/screenshots/ProcessesTab.png" width="700">

*Real-time CPU and memory monitoring for all running processes*

### Detail Views

**Startup Item Details**

<img src="docs/screenshots/StartupItemDetails.png" width="700">

*Simple explanations for what each startup item does*

<img src="docs/screenshots/StartupItemDetails2.png" width="700">

*Smart recommendations based on the item type*

**Process Details**

<img src="docs/screenshots/ProcessDetails.png" width="700">

*Detailed info for recognized processes*

<img src="docs/screenshots/ProcessDetails2.png" width="700">

*Safety warnings for critical system processes*

## How to Run

1. Clone or download this repo
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the app:
   ```bash
   ./scripts/run.sh
   ```

   Or directly with Python:
   ```bash
   PYTHONPATH=src python3 -m main
   ```

That's it. If you want to see system-level processes, run with `sudo`:
```bash
sudo PYTHONPATH=src python3 -m main
```

## Requirements

- macOS 10.14+
- Python 3.9+

## Tests

There's a test suite if you want to run it:
```bash
./scripts/run_tests.sh
```

Or use the Python test runner:
```bash
python3 scripts/run_tests.py
```

It has pretty good coverage (95%+) and tests most of the functionality. See [TESTING.md](docs/TESTING.md) for more details.

## Open Source

This is open source - feel free to fork it. If you add something, open a PR. If you find bugs, open an issue.

## What It Does

- Shows all your startup items (login items, launch agents, launch daemons)
- Lets you disable startup items you don't need
- Monitors running processes with real-time CPU/memory stats
- Shows system health with live charts and gauges

## Notes

- Custom fonts download automatically the first time you run it
- Charts update every 2 seconds
- Some operations need admin privileges (that's why there's a `sudo` option)
- Built with PyQt6 and psutil

---
