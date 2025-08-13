# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python import run_python_file


# def test():
#     test_dirs = [".", "pkg", "/bin","../"]
#     for dir in test_dirs:
#         print(f"Result for '{dir}' directory:")
#         content = get_files_info("calculator", dir)
#         if content.startswith("Error:"):
#             print(f"\t{content}")
#         else:
#             print(content)
#         print()

# def test():
#     test_files = [
#         "main.py",
#         "pkg/calculator.py",
#         "/bin/cat",
#         "pkg/does_not_exists.py",
#     ]
#     for file in test_files:
#         print(f"Content of file '{file}':")
#         print(get_file_content(working_directory="calculator", file_path=file))
#         print()

# def test():
#     test_data = [
#         ("lorem.txt", "wait, this isn't lorem ipsum"),
#         ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
#         ("/tmp/temp.txt", "this should not be allowed")
#     ]
#     for (file, text) in test_data:
#        print(f"Writing to file '{file}'...")
#        result = write_file(working_directory="calculator", file_path=file, content=text)
#        print(f"\t{result}")

def test():
    test_cases = [
        ("main.py", None),
        ("main.py", ["3 + 5"]),
        ("tests.py", None),
        ("../main.py", None),
        ("nonexistent.py", None),
    ]
    for (script, args) in test_cases:
        if args is None:
            args = []
        print(f"Run script {" ".join(["python3", script, *args])}:")
        result = run_python_file(working_directory="calculator", file_path=script, args=args)
        print(result)
test()
