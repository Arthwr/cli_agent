import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-2.0-flash-001"

if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
else:
    raise ValueError("Your must provide prompt argument")

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = client.models.generate_content(model=MODEL_NAME, contents=messages)


if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(f"\n{response.text}")
