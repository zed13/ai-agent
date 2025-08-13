import os

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
