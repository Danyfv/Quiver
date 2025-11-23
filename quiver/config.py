import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MENUS_DIR = BASE_DIR / "menus"
SCRIPTS_DIR = BASE_DIR / "scripts"
REPLACE_FILE = BASE_DIR / "replace.json"

def load_menus():
    """Loads all JSON menu files from the menus directory."""
    menus = {}
    if not MENUS_DIR.exists():
        return menus
    
    for file_path in MENUS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                menus[file_path.stem] = json.load(f)
        except Exception as e:
            print(f"Error loading menu {file_path}: {e}")
    return menus

def load_replacements():
    """Loads the replacement configuration."""
    if not REPLACE_FILE.exists():
        return {}
    try:
        with open(REPLACE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading replacements: {e}")
        return {}

def resolve_script_path(command):
    """Resolves the full path of a script/program."""
    # If it's an absolute path or exists relative to CWD
    if os.path.exists(command):
        return str(Path(command).resolve())
    
    # Check in scripts folder
    script_path = SCRIPTS_DIR / command
    if script_path.exists():
        return str(script_path.resolve())
    
    # Return as is (might be in PATH like notepad.exe)
    return command
