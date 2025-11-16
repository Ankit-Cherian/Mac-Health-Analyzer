# Mac Health Analyzer - Architecture Documentation

## Overview

Mac Health Analyzer is a PyQt6-based desktop application for macOS that provides system monitoring and startup item management with a distinctive, modern UI.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│           User Interface Layer          │
│   (PyQt6 Widgets, Custom Components)    │
├─────────────────────────────────────────┤
│          Application Layer              │
│    (Dashboard, Tabs, Controllers)       │
├─────────────────────────────────────────┤
│           Business Logic Layer          │
│  (StartupManager, ProcessMonitor)       │
├─────────────────────────────────────────┤
│           System Access Layer           │
│  (system_info.py, helpers.py)           │
├─────────────────────────────────────────┤
│              macOS APIs                 │
│  (launchctl, psutil, AppleScript)       │
└─────────────────────────────────────────┘
```

## Component Diagram

```
main.py
  └── MainWindow
       └── Dashboard
            ├── StartupTab
            │    └── StartupManager
            │         └── system_info.py
            ├── ProcessesTab
            │    └── ProcessMonitor
            │         └── helpers.py
            └── OverviewTab
                 └── ProcessMonitor + StartupManager
```

## Core Components

### 1. Main Application (`main.py`)
- **Purpose**: Entry point and main window
- **Responsibilities**:
  - Initialize application
  - Load fonts and styles
  - Create main window
  - Manage application lifecycle
- **Key Classes**: `MainWindow`, `QApplication`

### 2. Dashboard (`ui/dashboard.py`)
- **Purpose**: Central UI controller with tabbed interface
- **Responsibilities**:
  - Coordinate between tabs
  - Manage auto-refresh timers
  - Update system overview
- **Key Classes**: `Dashboard`

### 3. Startup Tab (`ui/startup_tab.py`)
- **Purpose**: UI for managing startup items
- **Responsibilities**:
  - Display startup items in table
  - Filter and search functionality
  - Disable/enable items
  - Show summary statistics
- **Key Classes**: `StartupTab`

### 4. Processes Tab (`ui/processes_tab.py`)
- **Purpose**: UI for monitoring processes
- **Responsibilities**:
  - Display running processes
  - Show resource usage metrics
  - Force quit processes
  - Filter and sort
- **Key Classes**: `ProcessesTab`

### 5. Startup Manager (`startup_manager.py`)
- **Purpose**: Business logic for startup items
- **Responsibilities**:
  - Fetch login items
  - Fetch Launch Agents/Daemons
  - Enable/disable items
  - Filter and search
- **Key Classes**: `StartupManager`

### 6. Process Monitor (`process_monitor.py`)
- **Purpose**: Business logic for process monitoring
- **Responsibilities**:
  - Fetch running processes
  - Calculate resource usage
  - Kill processes
  - Filter and sort
- **Key Classes**: `ProcessMonitor`

### 7. System Info (`utils/system_info.py`)
- **Purpose**: Low-level macOS system access
- **Responsibilities**:
  - Execute AppleScript
  - Parse plist files
  - Interact with launchctl
  - Query system events
- **Key Functions**: `get_login_items()`, `get_launch_agents()`, etc.

### 8. Helpers (`utils/helpers.py`)
- **Purpose**: Utility functions
- **Responsibilities**:
  - Process information via psutil
  - Format data
  - Calculate metrics
  - System resource queries
- **Key Functions**: `get_process_list()`, `get_system_memory_info()`, etc.

## UI Component Hierarchy

### Custom Widgets (`ui/widgets.py`)
- `ToggleSwitch`: Animated toggle with smooth transitions
- `StyledButton`: Enhanced QPushButton with custom styling
- `GlassmorphicPanel`: Semi-transparent panel with blur effect
- `MetricCard`: Card for displaying metrics
- `StatRow`: Row for label-value pairs
- `SearchBar`: Custom search input

### Styling System (`ui/styles.py`)
- **Color Palette**: Defined in `COLORS` dict
- **Main Stylesheet**: `get_main_stylesheet()`
- **Palette**: `get_palette()`
- **Dynamic Colors**: `get_status_color(percent)`

### Font Management (`ui/fonts.py`)
- **FontManager**: Singleton class
- **Fonts**: Bricolage Grotesque (display), JetBrains Mono (monospace)
- **Fallbacks**: System fonts if download fails
- **Methods**: `get_display_font()`, `get_mono_font()`

### Animations (`ui/animations.py`)
- **AnimationHelper**: Static methods for animations
- **Effects**: Fade in/out, staggered reveals, pulse
- **Framework**: QPropertyAnimation with QEasingCurve

## Data Flow

### Startup Items Flow
```
User Action
  ↓
StartupTab (UI)
  ↓
StartupManager (Logic)
  ↓
system_info.py (System Access)
  ↓
macOS APIs (launchctl, AppleScript)
  ↓
← Data Returns
```

### Process Monitoring Flow
```
Timer Trigger (every 2s)
  ↓
Dashboard (Controller)
  ↓
ProcessesTab (UI)
  ↓
ProcessMonitor (Logic)
  ↓
helpers.py (System Access)
  ↓
psutil (Library)
  ↓
← Process Data Returns
```

## Design Patterns

### 1. **Model-View Pattern**
- **Model**: StartupManager, ProcessMonitor
- **View**: StartupTab, ProcessesTab
- **Controller**: Dashboard

### 2. **Singleton Pattern**
- FontManager (global instance)

### 3. **Observer Pattern**
- Qt Signals/Slots for events
- Timer-based updates

### 4. **Factory Pattern**
- Widget creation methods (e.g., `create_table()`)

## Threading Model

- **Main Thread**: UI rendering and user interaction
- **Timer Events**: Non-blocking data refresh
- **System Calls**: Executed in main thread (fast enough)
- **Future Enhancement**: Move heavy operations to QThread

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Only refresh visible tabs
2. **Efficient Queries**: Cache startup items (rarely change)
3. **Smart Refresh**: Process monitor refreshes frequently
4. **Minimal Redraws**: Only update changed data
5. **Timer Management**: Different intervals for different data

### Resource Usage
- **Memory**: ~100-200MB (mostly Qt/PyQt overhead)
- **CPU**: <5% idle, <10% during refresh
- **Disk**: Minimal (fonts downloaded once)

## Security Considerations

### Permission Requirements
- **User-level**: Login items, user Launch Agents
- **Admin-level**: System Launch Agents/Daemons
- **Process Management**: Depends on process ownership

### Safety Mechanisms
1. Confirmation dialogs for destructive actions
2. Warnings before disabling system items
3. Graceful handling of permission denials
4. No data sent to external servers

## Extensibility Points

### Adding New Features
1. **New Tab**: Inherit from QWidget, add to Dashboard
2. **New Metric**: Extend ProcessMonitor or StartupManager
3. **New Widget**: Add to `ui/widgets.py`
4. **New System Query**: Add to `utils/system_info.py`

### Configuration
- Color palette: `ui/styles.py` → `COLORS` dict
- Refresh intervals: `ui/dashboard.py` → timer values
- Fonts: `ui/fonts.py` → `FONTS` dict

## Testing Strategy

### Unit Testing (Future)
- Test system_info functions
- Test helpers functions
- Mock macOS APIs

### Integration Testing
- Manual testing with checklist (see TESTING_GUIDE.md)
- Verify UI interactions
- Test error handling

### Performance Testing
- Monitor memory usage over time
- Check CPU usage during refresh
- Measure startup time

## Deployment

### Distribution Options
1. **Source Code**: Clone and run with Python
2. **PyInstaller**: Create standalone .app bundle
3. **py2app**: Native macOS application

### Dependencies
- PyQt6 (GUI framework)
- psutil (process monitoring)
- requests (font downloads)

## Future Enhancements

### Planned Features
1. Historical data tracking and graphs
2. Notification system for high resource usage
3. Startup time measurement
4. Recommendations engine
5. Export to CSV/JSON
6. Dark/Light theme toggle
7. Custom refresh intervals
8. Process priority management
9. Network usage monitoring
10. Disk usage analysis

### Technical Improvements
1. Async operations with QThread
2. Database for historical data (SQLite)
3. Unit test coverage
4. CI/CD pipeline
5. Auto-update mechanism
6. Crash reporting
7. Performance profiling
8. Accessibility improvements

## License and Credits

### Built With
- Python 3.9+
- PyQt6
- psutil
- Google Fonts (Bricolage Grotesque, JetBrains Mono)

### Design Philosophy
- Distinctive, non-generic UI
- Performance first
- User-friendly
- Mac-native feel
- Power user focused

