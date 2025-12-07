"""
Processes Tab UI for Mac Health Analyzer.
Displays and manages running processes with resource usage.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from ui.widgets import SearchBar, MetricCard, StyledButton
from ui.styles import COLORS, get_status_color
from ui.process_detail_dialog import ProcessDetailDialog
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
        self.is_updating = False  # Lock to prevent concurrent updates
        
        self.setup_ui()
        
        # Connect to search bar
        self.search_bar.search_changed.connect(self.on_search)
    
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
        
        # Sort buttons
        self.sort_cpu_btn = StyledButton("Sort by CPU", "secondary")
        self.sort_cpu_btn.clicked.connect(self.on_sort_by_cpu)
        header_layout.addWidget(self.sort_cpu_btn)
        
        self.sort_memory_btn = StyledButton("Sort by Memory", "secondary")
        self.sort_memory_btn.clicked.connect(self.on_sort_by_memory)
        header_layout.addWidget(self.sort_memory_btn)
        
        # Show system processes toggle
        self.system_processes_cb = QCheckBox("Include System Processes")
        self.system_processes_cb.stateChanged.connect(self.on_system_toggle)
        header_layout.addWidget(self.system_processes_cb)
        
        # Refresh button (now just triggers immediate data fetch attempt)
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
        
        # Search bar with hint
        search_layout = QHBoxLayout()
        self.search_bar = SearchBar("Search processes...")
        # search_changed connected in __init__
        search_layout.addWidget(self.search_bar)

        # Hint label
        hint_label = QLabel("Double-click any process to see detailed information")
        hint_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 12px;
            font-style: italic;
            padding: 4px 8px;
        """)
        search_layout.addWidget(hint_label)

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

        # Connect double-click to show details
        table.cellDoubleClicked.connect(self.on_process_double_clicked)

        return table
    
    @pyqtSlot()
    def update_data(self):
        """
        Update the table and metrics with current process data.
        Called when new data is available from the background worker.
        """
        # Skip if already updating or not visible (optimization)
        if self.is_updating or not self.isVisible():
            return
            
        try:
            self.is_updating = True
            # Data is now instant from cache
            self.current_processes = self.process_monitor.get_processes()
            self.apply_filters()
            self.update_metrics()
        except Exception as e:
            print(f"Error updating process data: {e}")
        finally:
            self.is_updating = False
    
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
            # Block signals during update for better performance
            self.table.blockSignals(True)
            
            # Remember selection
            selected_pids = {
                self.table.item(item.row(), 0).data(Qt.ItemDataRole.DisplayRole)
                for item in self.table.selectedItems()
            }
            
            self.table.setSortingEnabled(False)
            # Limit to 100 processes max for performance
            processes = processes[:100]
            self.table.setRowCount(len(processes))
            
            for row, proc in enumerate(processes):
                # PID
                pid_item = QTableWidgetItem(str(proc['pid']))
                pid_item.setData(Qt.ItemDataRole.DisplayRole, proc['pid'])
                self.table.setItem(row, 0, pid_item)
                
                # Restore selection
                if proc['pid'] in selected_pids:
                    pid_item.setSelected(True)
                
                # Name
                name_item = QTableWidgetItem(proc['name'])
                self.table.setItem(row, 1, name_item)
                if proc['pid'] in selected_pids:
                    name_item.setSelected(True)
                
                # Memory (human readable)
                memory_item = QTableWidgetItem(proc['memory_human'])
                memory_item.setData(Qt.ItemDataRole.DisplayRole, proc['memory_mb'])
                self.table.setItem(row, 2, memory_item)
                if proc['pid'] in selected_pids:
                    memory_item.setSelected(True)
                
                # Memory %
                mem_percent = proc['memory_percent']
                mem_percent_item = QTableWidgetItem(format_percentage(mem_percent))
                mem_percent_item.setData(Qt.ItemDataRole.DisplayRole, mem_percent)
                # Color code by usage
                if mem_percent > 10:
                    mem_percent_item.setForeground(self.get_color_for_percent(mem_percent))
                self.table.setItem(row, 3, mem_percent_item)
                if proc['pid'] in selected_pids:
                    mem_percent_item.setSelected(True)
                
                # CPU %
                cpu_percent = proc['cpu_percent']
                cpu_percent_item = QTableWidgetItem(format_percentage(cpu_percent))
                cpu_percent_item.setData(Qt.ItemDataRole.DisplayRole, cpu_percent)
                # Color code by usage
                if cpu_percent > 10:
                    cpu_percent_item.setForeground(self.get_color_for_percent(cpu_percent))
                self.table.setItem(row, 4, cpu_percent_item)
                if proc['pid'] in selected_pids:
                    cpu_percent_item.setSelected(True)
                
                # Store process data
                pid_item.setData(Qt.ItemDataRole.UserRole, proc)

            # Remember current sort state before re-enabling
            header = self.table.horizontalHeader()
            sort_column = header.sortIndicatorSection()
            sort_order = header.sortIndicatorOrder()

            # CRITICAL FIX: Clear sort indicator BEFORE re-enabling to prevent automatic re-sort
            # This prevents Qt from automatically sorting on the UI thread, which causes freezes
            header.setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)

            # Defer the sort operation to prevent blocking the UI thread
            # Default sort by memory usage if no sort was previously active
            if sort_column == -1:
                # No previous sort, apply default sort
                def apply_default_sort():
                    header.setSortIndicator(3, Qt.SortOrder.DescendingOrder)
                    self.table.sortItems(3, Qt.SortOrder.DescendingOrder)
                QTimer.singleShot(0, apply_default_sort)
            else:
                # Restore previous sort
                def apply_deferred_sort():
                    header.setSortIndicator(sort_column, sort_order)
                    self.table.sortItems(sort_column, sort_order)
                QTimer.singleShot(0, apply_deferred_sort)

        except Exception as e:
            print(f"Error populating process table: {e}")
            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)
    
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
    
    def on_sort_by_cpu(self):
        """Handle sort by CPU button click."""
        # Sort by CPU column (index 4) in descending order
        self.table.sortItems(4, Qt.SortOrder.DescendingOrder)
        
        # Update button styles to show active state
        self.sort_cpu_btn.setProperty("class", "primary")
        self.sort_memory_btn.setProperty("class", "secondary")
        # Force style update
        self.sort_cpu_btn.style().unpolish(self.sort_cpu_btn)
        self.sort_cpu_btn.style().polish(self.sort_cpu_btn)
        self.sort_memory_btn.style().unpolish(self.sort_memory_btn)
        self.sort_memory_btn.style().polish(self.sort_memory_btn)
    
    def on_sort_by_memory(self):
        """Handle sort by Memory button click."""
        # Sort by Memory % column (index 3) in descending order
        self.table.sortItems(3, Qt.SortOrder.DescendingOrder)
        
        # Update button styles to show active state
        self.sort_memory_btn.setProperty("class", "primary")
        self.sort_cpu_btn.setProperty("class", "secondary")
        # Force style update
        self.sort_memory_btn.style().unpolish(self.sort_memory_btn)
        self.sort_memory_btn.style().polish(self.sort_memory_btn)
        self.sort_cpu_btn.style().unpolish(self.sort_cpu_btn)
        self.sort_cpu_btn.style().polish(self.sort_cpu_btn)
    
    def on_refresh(self):
        """Handle refresh button click."""
        self.update_data()
    
    def on_system_toggle(self, state: int):
        """Handle system processes toggle."""
        include_system = state == Qt.CheckState.Checked.value
        self.process_monitor.set_include_system_processes(include_system)
        # The worker will update automatically next cycle
    
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
            
            # Refresh immediately
            self.on_refresh()

    def on_process_double_clicked(self, row: int, column: int):
        """
        Handle double-click on process row to show details.

        Args:
            row: Row index that was clicked
            column: Column index that was clicked
        """
        try:
            # Get process data from the row
            proc_data = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            if not proc_data:
                return

            # Get detailed process information
            pid = proc_data['pid']
            detailed_data = self.process_monitor.get_process_details(pid)

            if not detailed_data:
                QMessageBox.warning(
                    self,
                    "Process Not Found",
                    f"Could not retrieve details for process {proc_data['name']} (PID: {pid}). "
                    "It may have terminated."
                )
                return

            # Merge basic and detailed data
            full_data = {**proc_data, **detailed_data}

            # Show detail dialog
            dialog = ProcessDetailDialog(full_data, self)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to show process details: {str(e)}"
            )
