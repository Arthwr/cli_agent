import os
import sys
import time
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from config import MODEL_NAME, MAX_FN_CALLS
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do i build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    try:
        output = generate_content(client, messages, verbose)
        print("Final response: ", output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def generate_content(client, messages, verbose):
    message_history = messages.copy()
    function_call_index = 0

    while function_call_index < MAX_FN_CALLS:
        start = time.time()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message_history,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if verbose:
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)
            print(f"Function call round: {function_call_index + 1}")
            print(f"Duration {time.time() - start:.2f} seconds\n")

        for candidate in response.candidates:
            message_history.append(candidate.content)

        if not response.function_calls:
            if not response.text:
                raise ValueError("Model returned no text and no function calls.")
            return response.text

        fn_responses = []

        for fn in response.function_calls:
            fn_result_content = call_function(fn, verbose)

            if (
                not fn_result_content
                or not fn_result_content.parts[0].function_response.response
            ):
                raise ValueError("invalid function call result")

            if verbose:
                print(
                    "Result :",
                    json.dumps(
                        fn_result_content.parts[0].function_response.response.get(
                            "result", ""
                        ),
                        indent=2,
                    ),
                )

            fn_responses.append(fn_result_content)

        message_history.extend(fn_responses)
        function_call_index += 1

    raise RuntimeError(
        f"Reached maximum number of function calls without completing response: {MAX_FN_CALLS}"
    )


if __name__ == "__main__":
    main()
