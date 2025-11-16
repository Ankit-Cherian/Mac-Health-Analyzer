"""
Processes Tab UI for Mac Health Analyzer.
Displays and manages running processes with resource usage.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.widgets import SearchBar, MetricCard, StyledButton
from ui.styles import COLORS, get_status_color
from utils.helpers import format_percentage


class ProcessesTab(QWidget):
    """
    Tab for monitoring and managing processes.
    """
    
    refresh_requested = pyqtSignal()
    
    def __init__(self, process_monitor, parent=None):
        """
        Initialize processes tab.
        
        Args:
            process_monitor: ProcessMonitor instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.process_monitor = process_monitor
        self.current_processes = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Running Processes")
        title.setProperty("heading", "h2")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Show system processes toggle
        self.system_processes_cb = QCheckBox("Include System Processes")
        self.system_processes_cb.stateChanged.connect(self.on_system_toggle)
        header_layout.addWidget(self.system_processes_cb)
        
        # Refresh button
        self.refresh_btn = StyledButton("Refresh", "primary")
        self.refresh_btn.clicked.connect(self.on_refresh)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Metric cards
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        
        self.process_count_card = MetricCard("Total Processes", "0", "low")
        metrics_layout.addWidget(self.process_count_card)
        
        self.memory_card = MetricCard("Memory Usage", "0%", "low")
        metrics_layout.addWidget(self.memory_card)
        
        self.cpu_card = MetricCard("CPU Usage", "0%", "low")
        metrics_layout.addWidget(self.cpu_card)
        
        layout.addLayout(metrics_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_bar = SearchBar("Search processes...")
        self.search_bar.search_changed.connect(self.on_search)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)
        
        # Table
        self.table = self.create_table()
        layout.addWidget(self.table, stretch=1)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.quit_btn = StyledButton("Force Quit Selected", "danger")
        self.quit_btn.clicked.connect(self.on_force_quit)
        button_layout.addWidget(self.quit_btn)
        
        layout.addLayout(button_layout)
    
    def create_table(self) -> QTableWidget:
        """
        Create the processes table.
        
        Returns:
            QTableWidget configured for processes
        """
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["PID", "Name", "Memory", "Memory %", "CPU %"])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        
        # Column sizing
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # PID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Memory
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Memory %
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # CPU %
        
        # Enable sorting
        table.setSortingEnabled(True)
        
        return table
    
    def update_data(self):
        """Update the table and metrics with current process data."""
        try:
            self.process_monitor.refresh()
            self.current_processes = self.process_monitor.get_processes()
            self.apply_filters()
            self.update_metrics()
        except Exception as e:
            print(f"Error updating process data: {e}")
    
    def update_metrics(self):
        """Update metric cards."""
        summary = self.process_monitor.get_system_summary()
        
        # Process count
        count = summary['process_count']
        self.process_count_card.update_value(str(count), "low")
        
        # Memory usage
        mem_percent = summary['memory_percent']
        mem_status = self.get_status_from_percent(mem_percent)
        self.memory_card.update_value(
            format_percentage(mem_percent),
            mem_status
        )
        
        # CPU usage
        cpu_percent = summary['cpu_percent']
        cpu_status = self.get_status_from_percent(cpu_percent)
        self.cpu_card.update_value(
            format_percentage(cpu_percent),
            cpu_status
        )
    
    def get_status_from_percent(self, percent: float) -> str:
        """
        Get status level from percentage.
        
        Args:
            percent: Percentage value
            
        Returns:
            Status level ("low", "medium", "high")
        """
        if percent < 50:
            return "low"
        elif percent < 80:
            return "medium"
        else:
            return "high"
    
    def apply_filters(self):
        """Apply current search filter."""
        search_query = self.search_bar.text().lower()
        
        filtered_processes = self.current_processes.copy()
        
        # Apply search filter
        if search_query:
            filtered_processes = [
                proc for proc in filtered_processes
                if search_query in proc['name'].lower()
            ]
        
        self.populate_table(filtered_processes)
    
    def populate_table(self, processes: list):
        """
        Populate table with process data.
        
        Args:
            processes: List of process dicts
        """
        try:
            self.table.setSortingEnabled(False)
            self.table.setRowCount(len(processes))
            
            for row, proc in enumerate(processes):
                # PID
                pid_item = QTableWidgetItem(str(proc['pid']))
                pid_item.setData(Qt.ItemDataRole.DisplayRole, proc['pid'])
                self.table.setItem(row, 0, pid_item)
                
                # Name
                name_item = QTableWidgetItem(proc['name'])
                self.table.setItem(row, 1, name_item)
                
                # Memory (human readable)
                memory_item = QTableWidgetItem(proc['memory_human'])
                memory_item.setData(Qt.ItemDataRole.DisplayRole, proc['memory_mb'])
                self.table.setItem(row, 2, memory_item)
                
                # Memory %
                mem_percent = proc['memory_percent']
                mem_percent_item = QTableWidgetItem(format_percentage(mem_percent))
                mem_percent_item.setData(Qt.ItemDataRole.DisplayRole, mem_percent)
                # Color code by usage
                if mem_percent > 10:
                    mem_percent_item.setForeground(self.get_color_for_percent(mem_percent))
                self.table.setItem(row, 3, mem_percent_item)
                
                # CPU %
                cpu_percent = proc['cpu_percent']
                cpu_percent_item = QTableWidgetItem(format_percentage(cpu_percent))
                cpu_percent_item.setData(Qt.ItemDataRole.DisplayRole, cpu_percent)
                # Color code by usage
                if cpu_percent > 10:
                    cpu_percent_item.setForeground(self.get_color_for_percent(cpu_percent))
                self.table.setItem(row, 4, cpu_percent_item)
                
                # Store process data
                pid_item.setData(Qt.ItemDataRole.UserRole, proc)
            
            self.table.setSortingEnabled(True)
            # Default sort by memory usage
            self.table.sortItems(3, Qt.SortOrder.DescendingOrder)
        except Exception as e:
            print(f"Error populating process table: {e}")
            self.table.setSortingEnabled(True)
    
    def get_color_for_percent(self, percent: float):
        """
        Get QColor for percentage value.
        
        Args:
            percent: Percentage value
            
        Returns:
            QColor object
        """
        from PyQt6.QtGui import QColor
        color_hex = get_status_color(percent)
        return QColor(color_hex)
    
    def on_search(self, query: str):
        """Handle search query change."""
        self.apply_filters()
    
    def on_refresh(self):
        """Handle refresh button click."""
        self.update_data()
    
    def on_system_toggle(self, state: int):
        """Handle system processes toggle."""
        include_system = state == Qt.CheckState.Checked.value
        self.process_monitor.set_include_system_processes(include_system)
        self.update_data()
    
    def on_force_quit(self):
        """Handle force quit selected processes."""
        selected_rows = set(item.row() for item in self.table.selectedItems())
        
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Please select processes to force quit.")
            return
        
        # Get selected PIDs
        pids = []
        names = []
        for row in selected_rows:
            proc_data = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            pids.append(proc_data['pid'])
            names.append(proc_data['name'])
        
        # Confirm
        process_list = "\n".join([f"- {name} (PID: {pid})" for name, pid in zip(names, pids)])
        reply = QMessageBox.warning(
            self,
            "Confirm Force Quit",
            f"Are you sure you want to force quit these processes?\n\n{process_list}\n\n"
            "This may cause data loss if the applications have unsaved work.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success_count = 0
            for pid in pids:
                if self.process_monitor.kill_process(pid, force=True):
                    success_count += 1
            
            QMessageBox.information(
                self,
                "Force Quit Complete",
                f"Successfully force quit {success_count} of {len(pids)} process(es)."
            )
            
            # Refresh after a short delay
            self.on_refresh()

