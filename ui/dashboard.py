"""
Main Dashboard for Mac Health Analyzer - Neon Terminal Edition.
Enhanced with real-time charts, gauges, and cyberpunk visualizations.
"""

import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QLabel, QGridLayout, QScrollArea, QSplitter)
from PyQt6.QtCore import QTimer, Qt
from ui.startup_tab import StartupTab
from ui.processes_tab import ProcessesTab
from ui.animations import AnimationHelper
from ui.widgets import MetricCard, GlassmorphicPanel
from ui.charts import RealtimeLineChart, CircularGauge, BarChart


class Dashboard(QWidget):
    """
    Main dashboard with enhanced tabbed interface and visualizations.
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
        self._last_overview_refresh = 0.0

        self.setup_ui()
        self.setup_timers()

        # Connect tab change to stop updates when switching
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Initial data load
        self.load_initial_data()

    def on_tab_changed(self, index):
        """Handle tab change - refresh data for new tab."""
        current_widget = self.tab_widget.widget(index)
        if current_widget == self.processes_tab:
            self.processes_tab.update_data()
        elif current_widget == self.overview_tab:
            self.refresh_overview()

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

        # Add tabs with cyberpunk icons
        self.tab_widget.addTab(self.startup_tab, "⚡ STARTUP")
        self.tab_widget.addTab(self.processes_tab, "⚙ PROCESSES")

        # Create enhanced system overview tab
        self.overview_tab = self.create_enhanced_overview_tab()
        self.tab_widget.addTab(self.overview_tab, "◉ SYSTEM")

        layout.addWidget(self.tab_widget)

    def create_enhanced_overview_tab(self) -> QWidget:
        """
        Create enhanced system overview tab with charts and gauges.

        Returns:
            QWidget with enhanced system overview
        """
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title with neon styling
        title_container = QHBoxLayout()
        title = QLabel("◉ SYSTEM MONITOR")
        title.setProperty("heading", "h2")
        title_container.addWidget(title)
        title_container.addStretch()

        # Status indicator
        self.status_label = QLabel("● ONLINE")
        self.status_label.setProperty("heading", "h3")
        title_container.addWidget(self.status_label)

        main_layout.addLayout(title_container)

        # Create scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)

        # ==== TOP SECTION: CIRCULAR GAUGES ====
        gauges_layout = QHBoxLayout()
        gauges_layout.setSpacing(30)

        # CPU Gauge
        self.cpu_gauge = CircularGauge("CPU", "%")
        gauges_layout.addWidget(self.cpu_gauge)

        # Memory Gauge
        self.memory_gauge = CircularGauge("MEMORY", "%")
        gauges_layout.addWidget(self.memory_gauge)

        # Disk Gauge (processes count as proxy)
        self.processes_gauge = CircularGauge("PROCESSES", "")
        gauges_layout.addWidget(self.processes_gauge)

        gauges_layout.addStretch()

        scroll_layout.addLayout(gauges_layout)

        # ==== MIDDLE SECTION: REAL-TIME CHARTS ====
        charts_panel = GlassmorphicPanel()
        charts_layout = QVBoxLayout(charts_panel)

        charts_title = QLabel("▸ REAL-TIME MONITORING")
        charts_title.setProperty("heading", "h3")
        charts_layout.addWidget(charts_title)

        # Charts grid
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # CPU Chart
        self.cpu_chart = RealtimeLineChart("CPU Usage (%)", max_points=60)
        self.cpu_chart.setMinimumHeight(200)
        charts_grid.addWidget(self.cpu_chart, 0, 0)

        # Memory Chart
        self.memory_chart = RealtimeLineChart("Memory Usage (%)", max_points=60)
        self.memory_chart.setMinimumHeight(200)
        charts_grid.addWidget(self.memory_chart, 0, 1)

        charts_layout.addLayout(charts_grid)
        scroll_layout.addWidget(charts_panel)

        # ==== BOTTOM SECTION: RESOURCE BARS ====
        resources_panel = GlassmorphicPanel()
        resources_layout = QVBoxLayout(resources_panel)

        resources_title = QLabel("▸ TOP RESOURCE CONSUMERS")
        resources_title.setProperty("heading", "h3")
        resources_layout.addWidget(resources_title)

        # Bar charts grid
        bars_layout = QHBoxLayout()
        bars_layout.setSpacing(20)

        # Memory bar chart
        self.memory_bar_chart = BarChart("Top Memory")
        self.memory_bar_chart.setMinimumHeight(300)
        bars_layout.addWidget(self.memory_bar_chart)

        # CPU bar chart
        self.cpu_bar_chart = BarChart("Top CPU")
        self.cpu_bar_chart.setMinimumHeight(300)
        bars_layout.addWidget(self.cpu_bar_chart)

        resources_layout.addLayout(bars_layout)
        scroll_layout.addWidget(resources_panel)

        # ==== SYSTEM INFO CARDS ====
        info_panel = GlassmorphicPanel()
        info_layout = QGridLayout(info_panel)
        info_layout.setSpacing(15)

        info_title = QLabel("▸ SYSTEM INFORMATION")
        info_title.setProperty("heading", "h3")
        info_layout.addWidget(info_title, 0, 0, 1, 3)

        # Info metric cards
        self.total_memory_card = MetricCard("TOTAL RAM", "Loading...", "low")
        self.cpu_cores_card = MetricCard("CPU CORES", "Loading...", "low")
        self.startup_items_card = MetricCard("STARTUP ITEMS", "Loading...", "medium")

        info_layout.addWidget(self.total_memory_card, 1, 0)
        info_layout.addWidget(self.cpu_cores_card, 1, 1)
        info_layout.addWidget(self.startup_items_card, 1, 2)

        scroll_layout.addWidget(info_panel)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        return widget

    def setup_timers(self):
        """Set up auto-refresh timers."""
        # Process monitor refresh every 10 seconds (slower for stability)
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.refresh_processes)
        self.process_timer.start(10000)

        # Overview refresh every 2 seconds for real-time charts
        self.overview_timer = QTimer()
        self.overview_timer.timeout.connect(self.refresh_overview)
        self.overview_timer.start(2000)

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
        # Only refresh if processes tab is visible AND tab is visible to user
        try:
            if self.tab_widget.currentWidget() == self.processes_tab and self.isVisible():
                self.processes_tab.update_data()
        except Exception as e:
            print(f"Error refreshing processes: {e}")

    def refresh_overview(self):
        """Refresh overview data with enhanced visualizations."""
        try:
            # Only refresh if overview tab is active
            if self.tab_widget.currentWidget() != self.overview_tab:
                return

            now = time.time()
            if now - self._last_overview_refresh > 1.0:
                self.process_monitor.refresh()
                self._last_overview_refresh = now

            # Get system info
            mem_info = self.process_monitor.get_memory_info()
            cpu_info = self.process_monitor.get_cpu_info()

            # Update gauges
            cpu_percent = cpu_info.get('percent', 0.0)
            self.cpu_gauge.set_value(cpu_percent, 100)

            memory_percent = mem_info.get('percent', 0.0)
            self.memory_gauge.set_value(memory_percent, 100)

            process_count = self.process_monitor.get_process_count()
            self.processes_gauge.set_value(process_count, 500)  # Max 500 processes

            # Update real-time charts
            self.cpu_chart.update_data(cpu_percent)
            self.memory_chart.update_data(memory_percent)

            # Update info cards
            self.total_memory_card.update_value(
                mem_info.get('total_human', 'N/A'),
                "low"
            )

            self.cpu_cores_card.update_value(
                f"{cpu_info.get('count_logical', 0)}",
                "low"
            )

            startup_summary = self.startup_manager.get_summary()
            startup_status = "high" if startup_summary['enabled'] > 20 else "medium" if startup_summary['enabled'] > 10 else "low"
            self.startup_items_card.update_value(
                str(startup_summary['total']),
                startup_status
            )

            # Update bar charts
            top_memory = self.process_monitor.get_top_memory_processes(8)
            memory_data = []
            for proc in top_memory:
                label = proc['name'][:10]  # Truncate name
                value = proc.get('memory_percent', 0.0)
                memory_data.append((label, value, 100))

            self.memory_bar_chart.set_data(memory_data)

            top_cpu = self.process_monitor.get_top_cpu_processes(8)
            cpu_data = []
            for proc in top_cpu:
                label = proc['name'][:10]
                value = proc.get('cpu_percent', 0.0)
                cpu_data.append((label, value, 100))

            self.cpu_bar_chart.set_data(cpu_data)

            # Update status label
            self.status_label.setText("● ONLINE")

        except Exception as e:
            print(f"Error refreshing overview: {e}")
            self.status_label.setText("● ERROR")

    def cleanup(self):
        """Clean up resources."""
        try:
            self.process_timer.stop()
            self.overview_timer.stop()
        except Exception:
            pass
