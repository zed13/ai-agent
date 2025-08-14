from google.genai import types
import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    child_path = os.path.abspath(full_path)
    parent_path = os.path.abspath(working_directory)
    if not child_path.startswith(parent_path):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(full_path):
        return f"Error: \"{directory}\" is not a directory"
    try:
        report = []
        for entry in os.listdir(full_path):
             entry_path = os.path.join(full_path, entry)
             report.append(f" - {entry}: file_size={os.path.getsize(entry_path)} bytes, is_dir={os.path.isdir(entry_path)}")
        return "\n".join(report)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
