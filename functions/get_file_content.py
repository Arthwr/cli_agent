import os

from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) == MAX_CHARS:
                file_content_string += (
                    f"[...File {file_path} truncated at {MAX_CHARS} characters]"
                )

        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}" content: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        f"Reads and returns the text content of the specified file. "
        f"If the file content exceeds {MAX_CHARS} characters, the result will be truncated and noted. "
        f"Access is restricted to files within the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative file path (from the working directory) of the file to read. "
                    "The file must exist."
                ),
            )
        },
        required=["file_path"],
    ),
)
