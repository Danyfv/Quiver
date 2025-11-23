STYLESHEET = """
QMainWindow {
    background-color: rgba(43, 43, 43, 240);
    border: 2px solid #4CAF50;
    border-radius: 12px;
}

QLineEdit {
    background-color: #3c3f41;
    color: #e6e6e6;
    border: none;
    padding: 8px;
    font-size: 14px;
    font-family: "Segoe UI", sans-serif;
}

QListWidget {
    background-color: #2b2b2b;
    color: #e6e6e6;
    border: none;
    font-size: 13px;
    font-family: "Segoe UI", sans-serif;
}

QListWidget::item {
    padding: 5px;
}

QListWidget::item:selected {
    background-color: #4b6eaf;
    color: white;
}

QTabWidget::pane {
    border: none;
}

QTabBar::tab {
    background: #2b2b2b;
    color: #888;
    padding: 5px 10px;
    border: none;
}

QTabBar::tab:selected {
    color: #e6e6e6;
    background: #3c3f41;
}

QPushButton {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: bold;
    font-family: "Segoe UI", sans-serif;
}

QPushButton:hover {
    background-color: #4b6eaf;
    color: white;
    border-color: #4b6eaf;
}

QPushButton:pressed {
    background-color: #365880;
}

QListWidget {
    background-color: #2b2b2b;
    color: #e6e6e6;
    border: none;
    font-size: 14px;
    font-family: "Segoe UI", sans-serif;
    outline: none;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3c3f41;
}

QListWidget::item:selected {
    background-color: #4b6eaf;
    color: white;
    border-radius: 4px;
    border-bottom: none;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #a9b7c6;
    border: 1px solid #444;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 12px;
    margin-top: 5px;
}
"""
