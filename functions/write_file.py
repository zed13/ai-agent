import os
from google.genai import types

def write_file(working_directory, file_path, content):
   try:
       rel_file_path = os.path.join(working_directory, file_path)
       abs_work_dir = os.path.abspath(working_directory)
       abs_file_path = os.path.abspath(rel_file_path)
       if not abs_file_path.startswith(abs_work_dir):
           return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
       (dir_path, _) = os.path.split(abs_file_path)
       if not os.path.exists(dir_path):
           os.makedirs(dir_path)
       with open(abs_file_path, "w") as f:
           f.write(content)
       return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
   except Exception as e:
      return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Replaces content of the file with other content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content for replacing in file_path",
            )
        },
    ),
)
