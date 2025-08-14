import config
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info
from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content
from functions.write_file import schema_write_file
from functions.write_file import write_file
from functions.run_python import schema_run_python
from functions.run_python import run_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)

def main():
    if len(sys.argv) == 1:
       print("You should run it as: uv run main.py <prompt>")
       exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        )
    )

    if len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            match (function_call_part.name):
                case ("get_files_info"):
                    result = get_files_info(config.WORKING_DIR, function_call_part.args.get("directory", "."))
                    print(result)
                case ("get_file_content"):
                    result = get_file_content(config.WORKING_DIR, function_call_part.args["file_path"])
                    print(result)
                case ("write_file"):
                    result = write_file(config.WORKING_DIR, function_call_part.args["file_path"], function_call_part.args["content"])
                    print(result)
                case ("run_python"):
                    file_path = function_call_part.args["file_path"]
                    script_args = function_call_part.args["args"]
                    result = run_python_file(config.WORKING_DIR, file_path, script_args)
                    print(result)
                case _:
                    print(f"Unknow function request: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
