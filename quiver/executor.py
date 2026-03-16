import subprocess
import sys
import os
from .config import resolve_script_path

def execute_command(item):
    """
    Executes the command specified in the item dictionary.
    Returns a tuple (success, output_or_error).
    """
    cmd_type = item.get("type")
    
    try:
        # Verifico prima le operazioni di copy
        if cmd_type == "text":
            # Return text content directly
            content = item.get("content", "")
            return True, content
        elif cmd_type == "python":
            # Run with the same python interpreter
            command = item.get("command")
            if not command:
                return False, "No command specified."

            resolved_path = resolve_script_path(command)

            result = subprocess.run(
                [sys.executable, resolved_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(resolved_path) if os.path.isabs(resolved_path) else None,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        elif cmd_type == "bat":
            # Run bat file
            command = item.get("command")
            if not command:
                return False, "No command specified."
            resolved_path = resolve_script_path(command)
            result = subprocess.run(
                [resolved_path],
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(resolved_path) if os.path.isabs(resolved_path) else None,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        elif cmd_type == "program":
            # Run program
            # For programs, we might not want to wait for output if it's a GUI app
            # But the requirement says "replace output", implying we expect output.
            # However, "notepad.exe" doesn't give stdout.
            # If it's a GUI app, we probably just launch it.
            # But the prompt says "replace output... e.g. date".
            # I'll assume if it returns immediately, we capture output.
            # If it's a long running process, this might block.
            # For now, I'll treat it as a blocking call to capture output.
            command = item.get("command")
            if not command:
                return False, "No command specified."
            resolved_path = resolve_script_path(command)
            
            result = subprocess.run(
                [resolved_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(resolved_path) if os.path.isabs(resolved_path) else None,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            return False, f"Unknown type: {cmd_type}"

        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or "Error executing command."

    except Exception as e:
        return False, str(e)
