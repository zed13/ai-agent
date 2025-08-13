import os
import config

def get_file_content(working_directory, file_path, max_chars=config.MAX_CHARS):
   try:
        rel_file_path = os.path.join(working_directory, file_path)
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(rel_file_path)
        if not abs_file_path.startswith(abs_work_dir):
           return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
        if not os.path.isfile(abs_file_path):
           return f"Error: File not found or is not a regular file: '{file_path}'"
        file_content = ""
        with open(abs_file_path, "r") as f:
           file_content = f.read()
        if len(file_content) > max_chars:
           file_content = f"{file_content[:max_chars]}[...File '{file_path}' truncated at {max_chars} characters]"
        return file_content
   except Exception as e:
       return f"Error: {e}"
