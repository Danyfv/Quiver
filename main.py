import sys
import os
import keyboard
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, pyqtSignal

from quiver.ui.window import QuiverWindow

import json

# Paths to icons
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "quiver", "resources")
ICON_GREEN = os.path.join(RESOURCES_DIR, "icon_green.png")
ICON_BLUE = os.path.join(RESOURCES_DIR, "icon_blue.png")
ICON_RED = os.path.join(RESOURCES_DIR, "icon_red.png")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

class HotkeyHandler(QObject):
    show_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hotkey = "alt+q" # Default
        self.load_config()
        
        try:
            keyboard.add_hotkey(self.hotkey, self.on_hotkey)
        except ImportError:
            print("Keyboard library not found or error.")
        except Exception as e:
            print(f"Error setting hotkey: {e}")

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.hotkey = data.get("hotkey", "alt+q")
            except Exception as e:
                print(f"Error loading config: {e}")

    def on_hotkey(self):
        self.show_signal.emit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep running when window is hidden
    
    # Load Icons
    icon_green = QIcon(ICON_GREEN) if os.path.exists(ICON_GREEN) else QIcon()
    icon_blue = QIcon(ICON_BLUE) if os.path.exists(ICON_BLUE) else QIcon()
    icon_red = QIcon(ICON_RED) if os.path.exists(ICON_RED) else QIcon()
    
    app.setWindowIcon(icon_green)

    window = QuiverWindow()
    
    # System Tray Icon
    tray_icon = QSystemTrayIcon(icon_green, app)
    tray_icon.setToolTip("Quiver")
    
    def update_icon(status):
        if status == "running":
            tray_icon.setIcon(icon_blue)
            app.setWindowIcon(icon_blue)
        elif status == "error":
            tray_icon.setIcon(icon_red)
            app.setWindowIcon(icon_red)
        else:
            tray_icon.setIcon(icon_green)
            app.setWindowIcon(icon_green)
            
    window.status_changed.connect(update_icon)
    
    tray_menu = QMenu()
    show_action = tray_menu.addAction("Show")
    show_action.triggered.connect(window.show)
    show_action.triggered.connect(window.activateWindow)
    show_action.triggered.connect(window.raise_)
    
    quit_action = tray_menu.addAction("Quit")
    quit_action.triggered.connect(app.quit)
    
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()
    
    # Connect tray activation (double click)
    def tray_activated(reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            window.show()
            window.activateWindow()
            window.raise_()
            
    tray_icon.activated.connect(tray_activated)

    handler = HotkeyHandler()
    
    def toggle_window():
        if window.isVisible() and window.isActiveWindow():
            window.hide()
        else:
            window.show()
            window.activateWindow()
            window.raise_()
            
    handler.show_signal.connect(toggle_window)
    
    print(f"Quiver is running. Press {handler.hotkey} to open.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
