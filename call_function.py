import json

from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    func_args = dict(function_call_part.args)
    func_args["working_directory"] = WORKING_DIR

    if not func_name or func_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    if verbose:
        print(f"\nCalling function: {func_name}")
        print("Args: ", json.dumps(func_args, indent=2))
    else:
        print(f" - Calling function: {func_name}")

    try:
        function_result = function_map[func_name](**func_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": function_result},
                )
            ],
        )

    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": str(e)},
                )
            ],
        )
