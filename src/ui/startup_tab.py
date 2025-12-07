"""
Startup Items Tab UI for Mac Health Analyzer.
Displays and manages login items, Launch Agents, and Launch Daemons.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHeaderView, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from ui.widgets import SearchBar, ToggleSwitch, GlassmorphicPanel, StyledButton
from ui.styles import COLORS
from ui.startup_detail_dialog import StartupDetailDialog


class StartupTab(QWidget):
    """
    Tab for managing startup items.
    """
    
    refresh_requested = pyqtSignal()
    
    def __init__(self, startup_manager, process_monitor, parent=None):
        """
        Initialize startup tab.
        
        Args:
            startup_manager: StartupManager instance
            process_monitor: ProcessMonitor instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.startup_manager = startup_manager
        self.process_monitor = process_monitor
        self.current_items = []
        
        self.setup_ui()
        
        # Connect to startup manager updates
        self.startup_manager.data_updated.connect(self.update_data)
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Startup Items")
        title.setProperty("heading", "h2")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = StyledButton("Refresh", "primary")
        self.refresh_btn.setToolTip("Refresh the startup items list")
        self.refresh_btn.clicked.connect(self.on_refresh)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Summary panel
        self.summary_panel = self.create_summary_panel()
        layout.addWidget(self.summary_panel)
        
        # Search and filter
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)
        
        self.search_bar = SearchBar("Search startup items...")
        self.search_bar.search_changed.connect(self.on_search)
        filter_layout.addWidget(self.search_bar, stretch=2)
        
        # Filter by type
        filter_label = QLabel("Filter:")
        filter_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Items", "Login Items", "Launch Agents", "Launch Daemons", "Enabled Only", "Disabled Only"])
        self.filter_combo.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.filter_combo, stretch=1)
        
        layout.addLayout(filter_layout)

        # Hint label
        hint_label = QLabel("Double-click any item to see detailed information and recommendations")
        hint_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; padding: 4px;")
        layout.addWidget(hint_label)

        # Table
        self.table = self.create_table()
        layout.addWidget(self.table, stretch=1)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.disable_btn = StyledButton("Disable Selected", "danger")
        self.disable_btn.clicked.connect(self.on_disable_selected)
        button_layout.addWidget(self.disable_btn)
        
        layout.addLayout(button_layout)
    
    def create_summary_panel(self) -> QWidget:
        """
        Create summary panel showing statistics.
        
        Returns:
            QWidget with summary information
        """
        panel = GlassmorphicPanel()
        layout = QHBoxLayout(panel)
        layout.setSpacing(40)
        
        self.total_label = QLabel("0")
        self.total_label.setProperty("heading", "h1")
        self.total_label.setProperty("mono", "true")
        
        self.enabled_label = QLabel("0")
        self.enabled_label.setProperty("heading", "h1")
        self.enabled_label.setProperty("status", "medium")
        self.enabled_label.setProperty("mono", "true")
        
        self.disabled_label = QLabel("0")
        self.disabled_label.setProperty("heading", "h1")
        self.disabled_label.setProperty("status", "low")
        self.disabled_label.setProperty("mono", "true")
        
        # Total
        total_layout = QVBoxLayout()
        total_title = QLabel("Total Items")
        total_title.setProperty("heading", "h3")
        total_layout.addWidget(total_title)
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)
        
        # Enabled
        enabled_layout = QVBoxLayout()
        enabled_title = QLabel("Enabled")
        enabled_title.setProperty("heading", "h3")
        enabled_layout.addWidget(enabled_title)
        enabled_layout.addWidget(self.enabled_label)
        layout.addLayout(enabled_layout)
        
        # Disabled
        disabled_layout = QVBoxLayout()
        disabled_title = QLabel("Disabled")
        disabled_title.setProperty("heading", "h3")
        disabled_layout.addWidget(disabled_title)
        disabled_layout.addWidget(self.disabled_label)
        layout.addLayout(disabled_layout)
        
        layout.addStretch()
        
        return panel
    
    def create_table(self) -> QTableWidget:
        """
        Create the startup items table.
        
        Returns:
            QTableWidget configured for startup items
        """
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Name", "Type", "Status", "Location", "Toggle"])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        
        # Column sizing
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Location
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Toggle
        table.setColumnWidth(4, 80)
        
        # Enable sorting
        table.setSortingEnabled(True)

        # Connect double-click handler
        table.cellDoubleClicked.connect(self.on_item_double_clicked)

        return table
    
    @pyqtSlot()
    def update_data(self):
        """Update the table with current startup items."""
        # Items are now pre-matched to processes in the background worker thread
        # No need to call match_items_to_processes here, avoiding UI freeze
        self.current_items = self.startup_manager.get_all_items()
        self.apply_filters()
        self.update_summary()

        # Re-enable button if it was disabled (after a refresh)
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("Refresh")
    
    def update_summary(self):
        """Update summary statistics."""
        summary = self.startup_manager.get_summary()
        self.total_label.setText(str(summary['total']))
        self.enabled_label.setText(str(summary['enabled']))
        self.disabled_label.setText(str(summary['disabled']))
    
    def apply_filters(self):
        """Apply current search and filter settings."""
        filter_type = self.filter_combo.currentText()
        search_query = self.search_bar.text().lower()
        
        # Get filtered items
        filtered_items = self.current_items.copy()
        
        # Apply type filter
        if filter_type == "Login Items":
            filtered_items = [item for item in filtered_items if item['type'] == 'Login Item']
        elif filter_type == "Launch Agents":
            filtered_items = [item for item in filtered_items if item['type'] == 'Launch Agent']
        elif filter_type == "Launch Daemons":
            filtered_items = [item for item in filtered_items if item['type'] == 'Launch Daemon']
        elif filter_type == "Enabled Only":
            filtered_items = [item for item in filtered_items if item.get('enabled', True)]
        elif filter_type == "Disabled Only":
            filtered_items = [item for item in filtered_items if not item.get('enabled', True)]
        
        # Apply search filter
        if search_query:
            filtered_items = [
                item for item in filtered_items
                if search_query in item['name'].lower()
                or search_query in item.get('label', '').lower()
            ]
        
        self.populate_table(filtered_items)
    
    def populate_table(self, items: list):
        """
        Populate table with startup items.

        Args:
            items: List of startup item dicts
        """
        # Remember current sort state before disabling
        header = self.table.horizontalHeader()
        sort_column = header.sortIndicatorSection()
        sort_order = header.sortIndicatorOrder()
        was_sorting_enabled = self.table.isSortingEnabled()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            # Name
            name_item = QTableWidgetItem(item['name'])
            self.table.setItem(row, 0, name_item)

            # Type
            type_item = QTableWidgetItem(item['type'])
            self.table.setItem(row, 1, type_item)

            # Status
            status_text = "Enabled" if item.get('enabled', True) else "Disabled"
            status_item = QTableWidgetItem(status_text)
            self.table.setItem(row, 2, status_item)

            # Location
            location = item.get('location', item.get('path', 'N/A'))
            location_item = QTableWidgetItem(location)
            self.table.setItem(row, 3, location_item)

            # Toggle switch (as text for now, could be custom widget)
            toggle_item = QTableWidgetItem("●" if item.get('enabled', True) else "○")
            toggle_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, toggle_item)

            # Store item data
            name_item.setData(Qt.ItemDataRole.UserRole, item)

        # CRITICAL FIX: Clear sort indicator BEFORE re-enabling to prevent automatic re-sort
        # This prevents Qt from automatically sorting on the UI thread, which causes freezes
        header.setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

        # Now it's safe to re-enable sorting without triggering a blocking sort operation
        if was_sorting_enabled:
            self.table.setSortingEnabled(True)

            # Defer the sort operation to the next event loop iteration
            # This prevents any potential blocking on the UI thread during refresh
            # The 0ms timer queues the sort, keeping the UI responsive
            if sort_column >= 0:
                def apply_deferred_sort():
                    header.setSortIndicator(sort_column, sort_order)
                    self.table.sortItems(sort_column, sort_order)
                QTimer.singleShot(0, apply_deferred_sort)
    
    def on_search(self, query: str):
        """Handle search query change."""
        self.apply_filters()
    
    def on_refresh(self):
        """Handle refresh button click."""
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Refreshing...")
        self.startup_manager.refresh()
        # Re-enable happens in update_data which is connected to the data_updated signal
    
    def on_disable_selected(self):
        """Handle disable selected items."""
        selected_rows = set(item.row() for item in self.table.selectedItems())
        
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Please select items to disable.")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Disable",
            f"Are you sure you want to disable {len(selected_rows)} item(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success_count = 0
            for row in selected_rows:
                item_data = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
                if self.startup_manager.disable_item(item_data):
                    success_count += 1
            
            QMessageBox.information(
                self,
                "Disabled Items",
                f"Successfully disabled {success_count} of {len(selected_rows)} item(s)."
            )
            
            # Refresh
            self.on_refresh()
    
    def on_item_double_clicked(self, row: int, column: int):
        """
        Handle double-click on a startup item.

        Args:
            row: Row number that was double-clicked
            column: Column number that was double-clicked
        """
        try:
            # Get item data from the first column
            table_item = self.table.item(row, 0)
            if table_item is None:
                return

            item_data = table_item.data(Qt.ItemDataRole.UserRole)

            if item_data:
                # Show detail dialog
                dialog = StartupDetailDialog(item_data, self)
                dialog.exec()
        except Exception as e:
            print(f"Error opening startup item details: {e}")
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to open item details: {str(e)}"
            )
