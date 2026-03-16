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
    
    raw_params = item.get("parameters", [])
    if isinstance(raw_params, str):
        import shlex
        params = shlex.split(raw_params)
    else:
        params = [str(p) for p in raw_params]
    
    try:
        # Verifico prima le operazioni di copy
        if cmd_type == "text" or cmd_type == "html":
            # Return text content directly
            content = item.get("content", "")
            return True, content
        elif cmd_type == "python":
            # Run with the sgame python interpreter
            command = item.et("command")
            if not command:
                return False, "No command specified."

            resolved_path = resolve_script_path(command)

            result = subprocess.run(
                [sys.executable, resolved_path] + params,
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
            
            # Using shell=False is safer with lists, or appending params to the string if shell=True is needed
            cmd_list = [resolved_path] + params
            
            result = subprocess.run(
                cmd_list,
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
            cmd_list = [resolved_path] + params
            
            result = subprocess.run(
                cmd_list,
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
