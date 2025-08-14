import os
from google.genai import types
import subprocess
import config

def run_python_file(working_directory, file_path, args=[], timeout=config.EXECUTION_TIMEOUT):
    try:
        rel_file_path = os.path.join(working_directory, file_path)
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(rel_file_path)
        if not abs_file_path.startswith(abs_work_dir):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.exists(abs_file_path):
            return f"Error: File \"{file_path}\" not found."
        if not abs_file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file."
        escaped_args = escape_args(args)
        try:
            result = subprocess.run(
                args=["python3", f"{abs_file_path}", *escaped_args],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=abs_work_dir,
            )
        except Exception as e:
            return f"Error: executing Python file: {e}"
        report = []
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            report.append("No output produced")
        else:
            report.append("STDOUT:")
            report.append(str(result.stdout))
            report.append("STDERR:")
            report.append(str(result.stderr))
        if result.returncode != 0:
            report.append(f"Process exited with code {result.code}")
        return "\n".join(report)
    except Exception as e:
        return f"Error: {e}"

def escape_args(args):
   processed = []
   for arg in args:
       if " " in arg:
           processed.append(f"'{arg}'")
       else:
           processed.append(arg)
   return args


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python script with specified arguments, constrained to the working directory. Excecution timeout for script is 30 seconds",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                min_items=0,
                max_items=20,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Array of arguments for script to run. Could be empty array if no args required.",
            )
        },
    ),
)
