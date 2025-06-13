# CLI Agent

CLI Agent is a command-line tool that uses Google Gemini to assist with coding tasks by making function calls such as listing files, reading file contents, running Python scripts, and writing files.

## Requirements

- Python 3.10+
- [google-genai](https://pypi.org/project/google-genai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set your `GEMINI_API_KEY` in a `.env` file.

## Usage

Run the agent with a prompt:
```
python main.py "your prompt here"
```
Optional: add `--verbose` for detailed output.

## Features

- Lists files and directories
- Reads file contents
- Executes Python files
- Writes or overwrites files

See [prompts.py](cli_agent/prompts.py) for system behavior rules.
