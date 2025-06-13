import os
import subprocess

from config import MAX_SECONDS_TIMEOUT
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    _, ext = os.path.splitext(abs_file_path)
    if ext != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)

        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=MAX_SECONDS_TIMEOUT,
            cwd=abs_working_directory,
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        f"Executes a Python script at the specified file path with optional command-line arguments."
        f"The file must be located within the working directory."
        f"Execution is sandboxed and limited to {MAX_SECONDS_TIMEOUT} seconds."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path (from the working directory) to the Python file to execute."
                    "The file must have a .py extension and be located inside the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description=(
                    "A list of string arguments to pass to the Python script. "
                    "This is an OPTIONAL parameter. Only include it in the function call if the user explicitly provides arguments. "
                    "Otherwise, OMIT this parameter entirely."
                ),
                default=[],
            ),
        },
        required=["file_path"],
    ),
)
