import os


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
