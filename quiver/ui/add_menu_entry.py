# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "PyQt6",
# ]
# ///

import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class AddEntryDialog(QWidget):
    def __init__(self, json_path, current_path):
        super().__init__()
        self.json_path = json_path
        self.current_path = current_path
        
        path_str = " > ".join(["Root"] + current_path)
        self.setWindowTitle(f"Add Menu Entry ({path_str})")
        
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #a9b7c6; font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel { color: #cc7832; font-weight: bold; }
            QLineEdit, QComboBox { background-color: #3c3f41; border: 1px solid #555; border-radius: 4px; padding: 4px; color: #a9b7c6; }
            QPushButton { background-color: #4C5052; color: #e6e6e6; border: 1px solid #555; padding: 6px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #5C6062; }
            QPushButton:pressed { background-color: #3C3F41; }
            QMessageBox { background-color: #2b2b2b; color: #a9b7c6; }
        """)
        
        self.resize(400, 200)
        
        layout = QVBoxLayout(self)

        # Header with Help Button
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        self.help_btn = QPushButton("ℹ️ Help / Aiuto")
        self.help_btn.setToolTip("Show instructions / Mostra le istruzioni")
        self.help_btn.setFixedSize(110, 30)
        self.help_btn.clicked.connect(self.show_help)
        header_layout.addWidget(self.help_btn)
        layout.addLayout(header_layout)
        
        # Label
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Label:"))
        self.label_input = QLineEdit()
        h1.addWidget(self.label_input)
        layout.addLayout(h1)
        
        # Type
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["text", "html", "python", "bat", "program", "menu"])
        h2.addWidget(self.type_combo)
        layout.addLayout(h2)
        
        # Command / Content
        h3 = QHBoxLayout()
        self.cmd_label = QLabel("Content:")
        h3.addWidget(self.cmd_label)
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Paste text or type script name...")
        h3.addWidget(self.cmd_input)
        layout.addLayout(h3)

        # Parameters
        h4 = QHBoxLayout()
        self.param_label = QLabel("Params (Optional):")
        h4.addWidget(self.param_label)
        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("e.g. --key value -flag")
        h4.addWidget(self.param_input)
        layout.addLayout(h4)
        
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.on_type_changed(self.type_combo.currentText())
        
        # Button
        self.add_btn = QPushButton("Add Entry")
        self.add_btn.clicked.connect(self.add_entry)
        layout.addWidget(self.add_btn)

    def show_help(self):
        help_text = """
<b>🇬🇧 English:</b>
<ul>
    <li><b>Label:</b> The name of the button that will appear in Quiver.</li>
    <li><b>Type:</b> The kind of action this entry will execute.
        <ul>
            <li><i>text:</i> Simply copies the "Content" to your clipboard.</li>
            <li><i>python/bat/program:</i> Executes a script/program. The "Command/Script" should be the filename (e.g., <code>myscript.py</code>). Quiver looks for it automatically in the <code>scripts</code> folder or your system PATH.</li>
            <li><i>menu:</i> Creates a new folder/submenu.</li>
        </ul>
    </li>
    <li><b>Content / Command:</b> The text to copy or the exact filename of the script/program to run.</li>
    <li><b>Params (Optional):</b> Command-line arguments to pass to the script (e.g. <code>--name John -v</code>). Only used for executable types.</li>
</ul>

<hr>

<b>🇮🇹 Italiano:</b>
<ul>
    <li><b>Label:</b> Il nome del pulsante che apparirà su Quiver.</li>
    <li><b>Type:</b> Il tipo di azione che questa voce eseguirà.
        <ul>
            <li><i>text:</i> Copia semplicemente il "Contenuto" negli appunti.</li>
            <li><i>python/bat/program:</i> Esegue uno script o programma. Il "Command/Script" deve essere il nome del file (es. <code>myscript.py</code>). Quiver lo cercherà automaticamente nella cartella <code>scripts</code> o nel PATH di sistema.</li>
            <li><i>menu:</i> Crea una nuova cartella/sottomenù.</li>
        </ul>
    </li>
    <li><b>Content / Command:</b> Il testo da copiare o il nome esatto del file/programma da eseguire.</li>
    <li><b>Params (Optional):</b> Argomenti da linea di comando da passare allo script (es. <code>--name John -v</code>). Vengono usati solo per i tipi eseguibili.</li>
</ul>
"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Help / Istruzioni")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(help_text)
        msg.exec()

    def on_type_changed(self, text):
        if text == "text" or text == "html":
            self.cmd_label.setText("Content:")
            self.cmd_input.setEnabled(True)
            self.param_input.setEnabled(False)
            self.param_input.setText("")
        elif text == "menu":
            self.cmd_label.setText("N/A (Submenu):")
            self.cmd_input.setText("")
            self.cmd_input.setEnabled(False)
            self.param_input.setEnabled(False)
            self.param_input.setText("")
        else:
            self.cmd_label.setText("Command/Script:")
            self.cmd_input.setEnabled(True)
            self.param_input.setEnabled(True)

    def add_entry(self):
        label = self.label_input.text().strip()
        itype = self.type_combo.currentText()
        cmd = self.cmd_input.text().strip()
        params = self.param_input.text().strip()
        
        if not label:
            QMessageBox.warning(self, "Error", "Label is required.")
            return
            
        new_item = {"label": label, "type": itype}
        if itype == "text" or itype == "html":
            new_item["content"] = cmd
        elif itype == "menu":
            new_item["items"] = []
        else:
            if not cmd:
                QMessageBox.warning(self, "Error", "Command is required.")
                return
            new_item["command"] = cmd
            if params:
                import shlex
                new_item["parameters"] = shlex.split(params)
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Navigate to correct submenu
            target_list = data
            for p in self.current_path:
                found = False
                for item in target_list:
                    if item.get("label") == p and item.get("type") == "menu":
                        if "items" not in item:
                            item["items"] = []
                        target_list = item["items"]
                        found = True
                        break
                if not found:
                    raise Exception(f"Could not find submenu '{p}'.")
            
            target_list.append(new_item)
            
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
            QMessageBox.information(self, "Success", f"Added '{label}' successfully.")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_menu_entry.py <json_path> <current_path_json_string>")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    
    json_path = sys.argv[1]
    current_path = json.loads(sys.argv[2])
    
    win = AddEntryDialog(json_path, current_path)
    win.show()
    sys.exit(app.exec())
