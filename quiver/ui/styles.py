STYLESHEET = """
QMainWindow {
    background-color: rgba(43, 43, 43, 220);
    border: 1px solid #444;
    border-radius: 10px;
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

QPushButton#LogButton {
    background-color: transparent;
    color: #888;
    border: none;
    font-weight: bold;
}

QPushButton#LogButton:hover {
    color: #e6e6e6;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #a9b7c6;
    border: none;
    font-family: Consolas, monospace;
    font-size: 12px;
}
"""
