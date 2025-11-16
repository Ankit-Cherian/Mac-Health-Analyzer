# Testing Guide for Mac Health Analyzer

## Pre-Testing Checklist

1. **System Requirements**:
   - macOS 10.14 or later
   - Python 3.9 or higher
   - At least 50MB of free disk space

2. **Installation Verification**:
   ```bash
   python3 --version  # Should be 3.9+
   pip3 install -r requirements.txt
   ```

## Running the Application

### Method 1: Direct Python Execution
```bash
python3 main.py
```

### Method 2: Using Launch Script
```bash
./run.sh
```

### Method 3: With Administrator Privileges
```bash
sudo python3 main.py
```

## Testing Checklist

### ✅ Initial Launch
- [ ] Application window opens without errors
- [ ] Window is centered on screen
- [ ] Welcome dialog appears
- [ ] Custom fonts load (or fallback fonts work)
- [ ] All three tabs are visible

### ✅ Startup Items Tab
- [ ] Tab loads successfully
- [ ] Summary panel shows correct counts
- [ ] Table displays login items
- [ ] Table displays Launch Agents
- [ ] Table displays Launch Daemons
- [ ] Search bar filters items correctly
- [ ] Filter dropdown works (All, Login Items, etc.)
- [ ] Refresh button updates data
- [ ] Selecting items enables "Disable Selected" button
- [ ] Disabling items shows confirmation dialog
- [ ] Column sorting works (click headers)

### ✅ Running Processes Tab
- [ ] Tab loads successfully
- [ ] Metric cards show correct values
- [ ] Process table displays running processes
- [ ] Memory and CPU percentages are accurate
- [ ] Color coding works (high usage = red/orange)
- [ ] Search bar filters processes
- [ ] "Include System Processes" toggle works
- [ ] Refresh button updates data
- [ ] Auto-refresh works (every 2 seconds)
- [ ] Selecting processes enables "Force Quit" button
- [ ] Force quit shows confirmation dialog
- [ ] Column sorting works

### ✅ System Overview Tab
- [ ] Tab loads successfully
- [ ] All metric cards display data
- [ ] Top resource consumers update
- [ ] Memory and CPU info are accurate
- [ ] Auto-refresh works (every 3 seconds)

### ✅ UI/UX Testing
- [ ] Dark theme displays correctly
- [ ] Gradient backgrounds are visible
- [ ] Glassmorphic panels have blur effect
- [ ] Buttons have hover effects
- [ ] Tables have alternating row colors
- [ ] Scrollbars are styled correctly
- [ ] Font weights are varied (200/300 vs 700/800)
- [ ] Monospace font used for technical data
- [ ] Status colors (blue/orange/red) work correctly
- [ ] Tab switching is smooth
- [ ] No lag when typing in search bars

### ✅ Performance Testing
- [ ] Application starts in < 5 seconds
- [ ] Memory usage is reasonable (< 200MB)
- [ ] CPU usage is low when idle (< 5%)
- [ ] UI remains responsive during refreshes
- [ ] No memory leaks during extended use
- [ ] Timers clean up properly on exit

### ✅ Edge Cases
- [ ] Handles empty startup items gracefully
- [ ] Handles no running processes (unlikely but test)
- [ ] Handles permission denied errors
- [ ] Handles network errors (for font downloads)
- [ ] Handles missing plist files
- [ ] Handles corrupted plist files
- [ ] Handles killing already-dead processes
- [ ] Handles disabling already-disabled items

### ✅ Error Handling
- [ ] Shows user-friendly error messages
- [ ] Doesn't crash on permissions errors
- [ ] Fallback fonts work if custom fonts fail
- [ ] Gracefully handles system command failures
- [ ] Logs errors appropriately

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"
**Solution**: Install dependencies
```bash
pip3 install -r requirements.txt
```

### Issue: "Permission Denied" when disabling items
**Solution**: Run with sudo
```bash
sudo python3 main.py
```

### Issue: Fonts not loading
**Solution**: 
- Check internet connection
- Fonts will download on first run
- Application falls back to system fonts if download fails

### Issue: Process list is empty
**Solution**: Enable "Include System Processes" checkbox

### Issue: Application is slow
**Solution**:
- Reduce auto-refresh rate (edit timer intervals in dashboard.py)
- Filter out system processes
- Close other resource-intensive applications

### Issue: Can't see Launch Daemons
**Solution**: Run with administrator privileges
```bash
sudo python3 main.py
```

## Performance Benchmarks

**Expected Performance**:
- Startup time: 2-5 seconds
- Memory usage: 100-200 MB
- CPU usage (idle): < 5%
- CPU usage (refreshing): < 10%
- Refresh latency: < 100ms

## Automated Testing Commands

```bash
# Check Python syntax
python3 -m py_compile *.py ui/*.py utils/*.py

# Check for common issues
python3 -m pylint *.py ui/*.py utils/*.py --disable=all --enable=E

# Test imports
python3 -c "import main; import startup_manager; import process_monitor"
```

## Reporting Issues

When reporting issues, include:
1. macOS version
2. Python version
3. Error message or screenshot
4. Steps to reproduce
5. Expected vs actual behavior

## Testing Sign-Off

Date: ___________
Tester: ___________
macOS Version: ___________
Python Version: ___________

All tests passed: [ ] Yes [ ] No

Notes:
_________________________________
_________________________________
_________________________________

