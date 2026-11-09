import os
import subprocess
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file (.py) in the working directory and returns its output. Can accept optional command-line arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the Python file to execute.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional command-line arguments to pass to the Python script.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        result = subprocess.run(command + (args if args else []), capture_output=True, text=True, cwd=working_dir_abs, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if result.stdout:
            output.append(f'STDOUT: {result.stdout}')
        if result.stderr:
            output.append(f'STDERR: {result.stderr}')
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        return "\n".join(output)
    except Exception as e:
        return f'Error: executing Python file: {str(e)}'