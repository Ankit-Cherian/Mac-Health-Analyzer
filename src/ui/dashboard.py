"""
Main Dashboard for Mac Health Analyzer - Neon Terminal Edition.
Enhanced with real-time charts, gauges, and cyberpunk visualizations.
"""

import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QLabel, QGridLayout, QScrollArea, QSplitter,
                             QSizePolicy)
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
        self._cached_top_memory = []  # Cache for top memory processes
        self._cached_top_cpu = []  # Cache for top CPU processes

        self.setup_ui()
        self.setup_timers()

        # Connect tab change to stop updates when switching
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Initial data load
        self.load_initial_data()

    def on_tab_changed(self, index):
        """Handle tab change - refresh data for new tab and manage timers."""
        current_widget = self.tab_widget.widget(index)

        # Stop all timers first
        self.process_timer.stop()
        self.overview_timer.stop()

        # Start appropriate timer and refresh data based on active tab
        if current_widget == self.processes_tab:
            self.process_timer.start(10000)  # Resume process timer
            self.processes_tab.update_data()
        elif current_widget == self.overview_tab:
            self.overview_timer.start(2000)  # Resume overview timer
            self.refresh_overview()
        # If startup tab is selected, both timers remain stopped

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

        # Charts grid with card-style panels to keep visuals consistent
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)
        charts_grid.setColumnStretch(0, 1)
        charts_grid.setColumnStretch(1, 1)

        chart_card_height = 280

        # CPU Chart
        cpu_chart_card = GlassmorphicPanel(variant="minimal")
        cpu_chart_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cpu_chart_card.setMinimumHeight(chart_card_height)
        cpu_chart_card.setMaximumHeight(chart_card_height)
        cpu_chart_layout = QVBoxLayout(cpu_chart_card)
        cpu_chart_layout.setContentsMargins(20, 20, 20, 20)
        cpu_chart_layout.setSpacing(12)

        self.cpu_chart = RealtimeLineChart("CPU Usage (%)", max_points=60)
        self.cpu_chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.cpu_chart.setFixedHeight(chart_card_height - 40)
        cpu_chart_layout.addWidget(self.cpu_chart)
        charts_grid.addWidget(cpu_chart_card, 0, 0)

        # Memory Chart
        memory_chart_card = GlassmorphicPanel(variant="minimal")
        memory_chart_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        memory_chart_card.setMinimumHeight(chart_card_height)
        memory_chart_card.setMaximumHeight(chart_card_height)
        memory_chart_layout = QVBoxLayout(memory_chart_card)
        memory_chart_layout.setContentsMargins(20, 20, 20, 20)
        memory_chart_layout.setSpacing(12)

        self.memory_chart = RealtimeLineChart("Memory Usage (%)", max_points=60)
        self.memory_chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.memory_chart.setFixedHeight(chart_card_height - 40)
        memory_chart_layout.addWidget(self.memory_chart)
        charts_grid.addWidget(memory_chart_card, 0, 1)

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
        self.memory_bar_chart.clicked.connect(self.on_memory_bar_clicked)
        bars_layout.addWidget(self.memory_bar_chart)

        # CPU bar chart
        self.cpu_bar_chart = BarChart("Top CPU")
        self.cpu_bar_chart.setMinimumHeight(300)
        self.cpu_bar_chart.clicked.connect(self.on_cpu_bar_clicked)
        bars_layout.addWidget(self.cpu_bar_chart)

        resources_layout.addLayout(bars_layout)
        scroll_layout.addWidget(resources_panel)

        # ==== SYSTEM INFO CARDS ====
        info_panel = GlassmorphicPanel()
        info_layout = QVBoxLayout(info_panel)
        info_layout.setSpacing(15)
        info_layout.setContentsMargins(20, 20, 20, 20)

        # Title with hint
        title_layout = QHBoxLayout()
        info_title = QLabel("▸ SYSTEM INFORMATION")
        info_title.setProperty("heading", "h3")
        title_layout.addWidget(info_title)
        title_layout.addStretch()

        # Hint text
        from ui.styles import COLORS
        hint_label = QLabel("Click cards for details")
        hint_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        title_layout.addWidget(hint_label)

        info_layout.addLayout(title_layout)

        # Cards grid
        cards_grid = QGridLayout()
        cards_grid.setSpacing(15)

        # Info metric cards
        self.total_memory_card = MetricCard("TOTAL RAM", "Loading...", "low")
        self.total_memory_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.total_memory_card.mouseReleaseEvent = lambda e: self._show_memory_info()

        self.cpu_cores_card = MetricCard("CPU CORES", "Loading...", "low")
        self.cpu_cores_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cpu_cores_card.mouseReleaseEvent = lambda e: self._show_cpu_info()

        self.startup_items_card = MetricCard("STARTUP ITEMS", "Loading...", "medium")
        self.startup_items_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.startup_items_card.mouseReleaseEvent = lambda e: self._show_startup_info()

        cards_grid.addWidget(self.total_memory_card, 0, 0)
        cards_grid.addWidget(self.cpu_cores_card, 0, 1)
        cards_grid.addWidget(self.startup_items_card, 0, 2)
        cards_grid.setColumnStretch(0, 1)
        cards_grid.setColumnStretch(1, 1)
        cards_grid.setColumnStretch(2, 1)

        info_layout.addLayout(cards_grid)

        scroll_layout.addWidget(info_panel)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        return widget

    def setup_timers(self):
        """Set up auto-refresh timers. Timers start/stop based on active tab."""
        # Process monitor refresh every 10 seconds (slower for stability)
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.refresh_processes)
        # Don't start automatically - will start when tab is activated

        # Overview refresh every 2 seconds for real-time charts
        self.overview_timer = QTimer()
        self.overview_timer.timeout.connect(self.refresh_overview)
        # Don't start automatically - will start when tab is activated

    def load_initial_data(self):
        """Load initial data for all tabs."""
        # Load startup items
        self.startup_manager.refresh()
        self.startup_tab.update_data()

        # Load processes
        self.process_monitor.refresh()
        self.processes_tab.update_data()

        # Update overview (without starting timer yet)
        self.refresh_overview()

        # Start timer for the initially active tab
        current_index = self.tab_widget.currentIndex()
        self.on_tab_changed(current_index)

    def refresh_processes(self):
        """Refresh process data."""
        # Only refresh if processes tab is visible AND widget is visible to user
        # Note: Timer is stopped when tab is not active, so this is a safety check
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

            # Update bar charts and cache process data
            # Use get_top_processes for better performance (single call instead of two)
            top_processes = self.process_monitor.get_top_processes(8)
            top_memory = top_processes['memory']
            top_cpu = top_processes['cpu']

            self._cached_top_memory = top_memory  # Cache retained for potential reuse
            memory_data = []
            for proc in top_memory:
                memory_data.append({
                    'label': proc['name'],
                    'value': proc.get('memory_percent', 0.0),
                    'max': 100,
                    'payload': proc
                })

            self.memory_bar_chart.set_data(memory_data)

            self._cached_top_cpu = top_cpu  # Cache retained for potential reuse
            cpu_data = []
            for proc in top_cpu:
                cpu_data.append({
                    'label': proc['name'],
                    'value': proc.get('cpu_percent', 0.0),
                    'max': 100,
                    'payload': proc
                })

            self.cpu_bar_chart.set_data(cpu_data)

            # Update status label
            self.status_label.setText("● ONLINE")

        except Exception as e:
            print(f"Error refreshing overview: {e}")
            self.status_label.setText("● ERROR")

    def on_memory_bar_clicked(self, entry: dict):
        """
        Handle double-click on memory bar chart.

        Args:
            entry: Data dictionary emitted by the chart
        """
        process_data = entry.get('payload')
        if process_data:
            self._show_process_detail(process_data)

    def on_cpu_bar_clicked(self, entry: dict):
        """
        Handle double-click on CPU bar chart.

        Args:
            entry: Data dictionary emitted by the chart
        """
        process_data = entry.get('payload')
        if process_data:
            self._show_process_detail(process_data)

    def _show_process_detail(self, process_data: dict):
        """
        Show process detail dialog.

        Args:
            process_data: Process information dictionary
        """
        from ui.process_detail_dialog import ProcessDetailDialog
        dialog = ProcessDetailDialog(process_data, self)
        dialog.exec()

    def _show_memory_info(self):
        """Show detailed memory information dialog."""
        from PyQt6.QtWidgets import QMessageBox
        mem_info = self.process_monitor.get_memory_info()

        total = mem_info.get('total_human', 'N/A')
        used = mem_info.get('used_human', 'N/A')
        available = mem_info.get('available_human', 'N/A')
        percent = mem_info.get('percent', 0)

        message = (
            f"<h3>Memory Information</h3>"
            f"<p><b>Total RAM:</b> {total}<br>"
            f"<b>Used:</b> {used} ({percent:.1f}%)<br>"
            f"<b>Available:</b> {available}</p>"
            f"<hr>"
            f"<p><i>What does this mean?</i><br>"
            f"Your Mac has {total} of total memory (RAM). "
            f"You're currently using {used}, which is {percent:.1f}% of your total memory. "
            f"The remaining {available} is available for other programs.</p>"
            f"<p><b>Tip:</b> If your memory usage is consistently above 80%, "
            f"consider closing unused applications or upgrading your RAM.</p>"
        )

        QMessageBox.information(self, "System Memory", message)

    def _show_cpu_info(self):
        """Show detailed CPU information dialog."""
        from PyQt6.QtWidgets import QMessageBox
        cpu_info = self.process_monitor.get_cpu_info()

        logical_cores = cpu_info.get('count_logical', 0)
        physical_cores = cpu_info.get('count_physical', 0)
        percent = cpu_info.get('percent', 0)

        message = (
            f"<h3>CPU Information</h3>"
            f"<p><b>Physical Cores:</b> {physical_cores}<br>"
            f"<b>Logical Cores:</b> {logical_cores}<br>"
            f"<b>Current Usage:</b> {percent:.1f}%</p>"
            f"<hr>"
            f"<p><i>What does this mean?</i><br>"
            f"Your Mac has {physical_cores} physical CPU cores and {logical_cores} logical cores. "
            f"Cores are like workers that can handle different tasks simultaneously. "
            f"More cores mean your Mac can handle more tasks at once.</p>"
            f"<p><b>Current Usage:</b> Your CPU is currently running at {percent:.1f}% capacity. "
            f"If this is consistently above 80%, your Mac might feel slow.</p>"
            f"<p><b>Tip:</b> Close applications you're not using to reduce CPU usage.</p>"
        )

        QMessageBox.information(self, "CPU Information", message)

    def _show_startup_info(self):
        """Show detailed startup items information dialog."""
        from PyQt6.QtWidgets import QMessageBox
        summary = self.startup_manager.get_summary()

        total = summary['total']
        enabled = summary['enabled']
        disabled = summary['disabled']

        message = (
            f"<h3>Startup Items</h3>"
            f"<p><b>Total Items:</b> {total}<br>"
            f"<b>Enabled:</b> {enabled}<br>"
            f"<b>Disabled:</b> {disabled}</p>"
            f"<hr>"
            f"<p><i>What are startup items?</i><br>"
            f"Startup items are programs that automatically start when you log in to your Mac. "
            f"While some are essential (like system services), others might not be necessary.</p>"
            f"<p><b>Current Status:</b> You have {enabled} enabled startup items. "
        )

        if enabled > 20:
            message += (
                f"This is quite high and might slow down your Mac's startup time.</p>"
                f"<p><b>Recommendation:</b> Consider disabling items you don't need. "
                f"Go to the STARTUP tab and double-click items to see if they're safe to disable.</p>"
            )
        elif enabled > 10:
            message += (
                f"This is a moderate amount. Your Mac should start reasonably quickly.</p>"
                f"<p><b>Tip:</b> Review your startup items occasionally and disable any you don't use.</p>"
            )
        else:
            message += (
                f"This is a healthy amount. Your Mac should start quickly!</p>"
            )

        QMessageBox.information(self, "Startup Items", message)

    def cleanup(self):
        """Clean up resources."""
        try:
            self.process_timer.stop()
            self.overview_timer.stop()
        except Exception:
            pass
