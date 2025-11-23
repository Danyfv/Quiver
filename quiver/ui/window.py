import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QListWidget, QTabWidget, QLabel, 
                             QFrame, QPushButton, QTextEdit, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QIcon, QColor, QAction

from ..config import load_menus, load_replacements
from ..executor import execute_command
from ..replacer import process_replacements
from .styles import STYLESHEET

class ExecutionThread(QThread):
    finished_signal = pyqtSignal(bool, str, str) # success, output, original_text

    def __init__(self, item, replace_config):
        super().__init__()
        self.item = item
        self.replace_config = replace_config

    def run(self):
        # 1. Execute the main command
        success, output = execute_command(self.item)
        
        if success:
            # 2. Process replacements
            try:
                final_output = process_replacements(output, self.replace_config)
                self.finished_signal.emit(True, final_output, output)
            except Exception as e:
                self.finished_signal.emit(False, f"Replacement Error: {e}", output)
        else:
            self.finished_signal.emit(False, output, "")

class QuiverWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiver")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(500, 400)
        
        # Data
        self.menus = load_menus()
        self.replace_config = load_replacements()
        self.current_items = []
        self.menu_stack = [] # Stack to track sub-menus
        self.old_pos = None
        
        # UI Setup
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet(STYLESHEET)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Title Bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(30)
        self.title_bar.setStyleSheet("background-color: #3c3f41; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(10, 0, 10, 0)
        
        self.title_label = QLabel("🏹 Quiver")
        self.title_label.setStyleSheet("color: #e6e6e6; font-weight: bold; border: none;")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.clicked.connect(self.hide)
        self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: #888; border: none; } QPushButton:hover { color: #F44336; }")
        self.title_layout.addWidget(self.close_btn)
        
        self.layout.addWidget(self.title_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.tabs.setFixedHeight(30)
        self.layout.addWidget(self.tabs)
        
        # Search
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_items)
        self.search_bar.returnPressed.connect(self.execute_selected)
        self.layout.addWidget(self.search_bar)
        
        # List
        self.list_widget = QListWidget()
        self.list_widget.itemActivated.connect(self.execute_selected)
        self.layout.addWidget(self.list_widget)
        
        # Status Line
        self.status_line = QFrame()
        self.status_line.setFixedHeight(4)
        self.set_status("idle") # idle/green, running/blue, error/red
        self.layout.addWidget(self.status_line)
        
        # Bottom Bar (Log Button)
        self.bottom_bar = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(5, 5, 5, 5)
        
        self.log_button = QPushButton("LOGS")
        self.log_button.setObjectName("LogButton")
        self.log_button.setFixedWidth(100)
        self.log_button.setStyleSheet("color: #899; border: none; font-weight: bold;")
        self.log_button.clicked.connect(self.toggle_logs)
        self.bottom_layout.addWidget(self.log_button)
        
        self.reload_button = QPushButton("RELOAD")
        self.reload_button.setFixedWidth(100)
        self.reload_button.clicked.connect(self.reload_config)
        self.reload_button.setStyleSheet("color: #899; border: none; font-weight: bold;")
        self.bottom_layout.addWidget(self.reload_button)

        self.bottom_layout.addStretch()
        
        self.quit_button = QPushButton("QUIT")
        self.quit_button.setFixedWidth(100)
        self.quit_button.clicked.connect(self.quit_app)
        self.quit_button.setStyleSheet("color: #899; border: 1px solid red; font-weight: bold;")
        self.bottom_layout.addWidget(self.quit_button)
        
        self.layout.addWidget(self.bottom_bar)
        
        # Log Area (Hidden by default)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.hide()
        self.layout.addWidget(self.log_area)
        
        # Populate Tabs
        self.populate_tabs()
        
        # Focus
        self.search_bar.setFocus()

    def populate_tabs(self):
        self.tabs.clear()
        if not self.menus:
            self.tabs.addTab(QWidget(), "No Menus")
            return

        for name, items in self.menus.items():
            tab = QWidget()
            self.tabs.addTab(tab, name)
            
        # Load initial items
        if self.menus:
            first_key = list(self.menus.keys())[0]
            self.current_items = self.menus[first_key]
            self.update_list()

    def get_display_label(self, item):
        itype = item.get("type", "unknown")
        label = item.get("label", "Unknown")
        
        icon = "🔹"
        if itype == "program": icon = "🚀"
        elif itype == "bat": icon = "⚙️"
        elif itype == "python": icon = "🐍"
        elif itype == "text": icon = "📝"
        elif itype == "menu": icon = "📁"
        
        return f"{icon}  {label}"

    def update_list(self):
        self.list_widget.clear()
        for item in self.current_items:
            self.list_widget.addItem(self.get_display_label(item))

    def on_tab_changed(self, index):
        tab_name = self.tabs.tabText(index)
        if tab_name in self.menus:
            self.current_items = self.menus[tab_name]
            self.menu_stack = [] # Reset stack on tab change
            self.filter_items(self.search_bar.text())

    def filter_items(self, text):
        self.list_widget.clear()
        
        if self.menu_stack:
            self.list_widget.addItem("🔙  .. (Back)")

        text = text.lower()
        for item in self.current_items:
            label = item.get("label", "Unknown")
            if text in label.lower():
                self.list_widget.addItem(self.get_display_label(item))
        
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def execute_selected(self):
        current_row = self.list_widget.currentRow()
        if current_row < 0:
            return
            
        item_text = self.list_widget.item(current_row).text()
        
        if "🔙" in item_text:
            self.go_back()
            return

        # Extract label (remove icon and spacing)
        # Assuming format "ICON  Label"
        parts = item_text.split("  ", 1)
        if len(parts) > 1:
            item_label = parts[1]
        else:
            item_label = item_text

        # Find item data
        selected_item = next((i for i in self.current_items if i["label"] == item_label), None)
        
        if selected_item:
            if selected_item.get("type") == "menu":
                self.enter_submenu(selected_item)
            else:
                self.run_command(selected_item)

    def run_command(self, item):
        self.set_status("running")
        self.log(f"Executing: {item.get('label')}")
        
        self.thread = ExecutionThread(item, self.replace_config)
        self.thread.finished_signal.connect(self.on_execution_finished)
        self.thread.start()

    def on_execution_finished(self, success, output, original):
        if success:
            self.set_status("success")
            self.log(f"Success. Output: {output}")
            QApplication.clipboard().setText(output)
        else:
            self.set_status("error")
            self.log(f"Error: {output}")

    status_changed = pyqtSignal(str)

    def set_status(self, status):
        self.status_changed.emit(status)
        if status == "idle" or status == "success":
            self.status_line.setStyleSheet("background-color: #4CAF50;") # Green
        elif status == "running":
            self.status_line.setStyleSheet("background-color: #2196F3;") # Blue
        elif status == "error":
            self.status_line.setStyleSheet("background-color: #F44336;") # Red

    def log(self, message):
        self.log_area.append(message)

    def toggle_logs(self):
        if self.log_area.isVisible():
            self.log_area.hide()
            self.resize(600, 400)
        else:
            self.log_area.show()
            self.resize(600, 600)

    def enter_submenu(self, item):
        self.menu_stack.append(self.current_items)
        self.current_items = item.get("items", [])
        self.search_bar.clear()
        self.filter_items("")

    def go_back(self):
        if self.menu_stack:
            self.current_items = self.menu_stack.pop()
            self.search_bar.clear()
            self.filter_items("")

    def reload_config(self):
        self.menus = load_menus()
        self.replace_config = load_replacements()
        self.populate_tabs()
        self.log("Configuration reloaded.")

    def quit_app(self):
        QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    # Dragging Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
