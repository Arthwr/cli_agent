import os


def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    directory_path = os.path.abspath(
        os.path.join(abs_working_directory, directory or "")
    )

    if not directory_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory_path):
        return f"Error: {directory or "."} is not a directory"

    try:
        files = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            file_info = f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}"
            files.append(file_info)

        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"
