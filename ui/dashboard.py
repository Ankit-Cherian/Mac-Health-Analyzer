"""
Main Dashboard for Mac Health Analyzer.
Central component with tabbed interface.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel
from PyQt6.QtCore import QTimer
from ui.startup_tab import StartupTab
from ui.processes_tab import ProcessesTab
from ui.animations import AnimationHelper


class Dashboard(QWidget):
    """
    Main dashboard with tabbed interface.
    """
    
    def __init__(self, startup_manager, process_monitor, parent=None):
        """
        Initialize dashboard.
        
        Args:
            startup_manager: StartupManager instance
            process_monitor: ProcessMonitor instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.startup_manager = startup_manager
        self.process_monitor = process_monitor
        
        self.setup_ui()
        self.setup_timers()
        
        # Initial data load
        self.load_initial_data()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.startup_tab = StartupTab(self.startup_manager)
        self.processes_tab = ProcessesTab(self.process_monitor)
        
        # Add tabs
        self.tab_widget.addTab(self.startup_tab, "⚡ Startup Items")
        self.tab_widget.addTab(self.processes_tab, "📊 Running Processes")
        
        # Create system overview tab
        self.overview_tab = self.create_overview_tab()
        self.tab_widget.addTab(self.overview_tab, "🖥️ System Overview")
        
        layout.addWidget(self.tab_widget)
    
    def create_overview_tab(self) -> QWidget:
        """
        Create system overview tab.
        
        Returns:
            QWidget with system overview
        """
        from PyQt6.QtWidgets import QGridLayout
        from ui.widgets import MetricCard, GlassmorphicPanel
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("System Overview")
        title.setProperty("heading", "h2")
        layout.addWidget(title)
        
        # Metrics grid
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(20)
        
        # Create metric cards
        self.overview_memory_card = MetricCard("Total Memory", "Loading...", "low")
        self.overview_cpu_card = MetricCard("CPU Cores", "Loading...", "low")
        self.overview_processes_card = MetricCard("Active Processes", "Loading...", "low")
        self.overview_startup_card = MetricCard("Startup Items", "Loading...", "medium")
        
        metrics_layout.addWidget(self.overview_memory_card, 0, 0)
        metrics_layout.addWidget(self.overview_cpu_card, 0, 1)
        metrics_layout.addWidget(self.overview_processes_card, 1, 0)
        metrics_layout.addWidget(self.overview_startup_card, 1, 1)
        
        layout.addLayout(metrics_layout)
        
        # Top resource consumers
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        
        panel_title = QLabel("Top Resource Consumers")
        panel_title.setProperty("heading", "h3")
        panel_layout.addWidget(panel_title)
        
        self.top_memory_label = QLabel("Loading...")
        self.top_memory_label.setProperty("mono", "true")
        panel_layout.addWidget(self.top_memory_label)
        
        self.top_cpu_label = QLabel("Loading...")
        self.top_cpu_label.setProperty("mono", "true")
        panel_layout.addWidget(self.top_cpu_label)
        
        layout.addWidget(panel)
        layout.addStretch()
        
        return widget
    
    def setup_timers(self):
        """Set up auto-refresh timers."""
        # Process monitor refresh every 3 seconds (increased from 2)
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.refresh_processes)
        self.process_timer.start(3000)
        
        # Overview refresh every 5 seconds (increased from 3)
        self.overview_timer = QTimer()
        self.overview_timer.timeout.connect(self.refresh_overview)
        self.overview_timer.start(5000)
    
    def load_initial_data(self):
        """Load initial data for all tabs."""
        # Load startup items
        self.startup_manager.refresh()
        self.startup_tab.update_data()
        
        # Load processes
        self.process_monitor.refresh()
        self.processes_tab.update_data()
        
        # Update overview
        self.refresh_overview()
    
    def refresh_processes(self):
        """Refresh process data."""
        # Only refresh if processes tab is visible
        try:
            if self.tab_widget.currentWidget() == self.processes_tab:
                self.processes_tab.update_data()
        except Exception as e:
            print(f"Error refreshing processes: {e}")
    
    def refresh_overview(self):
        """Refresh overview data."""
        try:
            # Update system info
            mem_info = self.process_monitor.get_memory_info()
            cpu_info = self.process_monitor.get_cpu_info()
            
            self.overview_memory_card.update_value(
                mem_info.get('total_human', 'N/A'),
                "low"
            )
        
            self.overview_cpu_card.update_value(
                f"{cpu_info.get('count_logical', 0)} cores",
                "low"
            )
            
            self.overview_processes_card.update_value(
                str(self.process_monitor.get_process_count()),
                "low"
            )
            
            startup_summary = self.startup_manager.get_summary()
            startup_status = "medium" if startup_summary['enabled'] > 10 else "low"
            self.overview_startup_card.update_value(
                str(startup_summary['total']),
                startup_status
            )
            
            # Top consumers
            top_memory = self.process_monitor.get_top_memory_processes(3)
            top_cpu = self.process_monitor.get_top_cpu_processes(3)
            
            mem_text = "Top Memory Consumers:\n"
            for proc in top_memory:
                mem_text += f"  • {proc['name']}: {proc['memory_human']}\n"
            self.top_memory_label.setText(mem_text)
            
            cpu_text = "Top CPU Consumers:\n"
            for proc in top_cpu:
                cpu_text += f"  • {proc['name']}: {proc['cpu_percent']:.1f}%\n"
            self.top_cpu_label.setText(cpu_text)
        except Exception as e:
            print(f"Error refreshing overview: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.process_timer.stop()
            self.overview_timer.stop()
        except Exception:
            pass

