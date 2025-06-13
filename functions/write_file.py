import os

from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{abs_file_path}" as it is outside the permitted working directory'

    try:
        file_dirname = os.path.dirname(abs_file_path)

        if not os.path.exists(file_dirname):
            os.makedirs(file_dirname)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writting file {abs_file_path} content: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes content to a specified file path. If the file or its directories don't exist, they will be created."
        "All write operations are restricted to the defined working directory for safety. Returns a success or error message."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative file path (from the working directory) where the content should be written."
                    "Directories in the path will be created if they don't exist."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to be written to the specified file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
