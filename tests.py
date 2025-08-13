from functions.get_files_info import get_files_info


def test():
    test_dirs = [".", "pkg", "/bin","../"]
    for dir in test_dirs:
        print(f"Result for '{dir}' directory:")
        content = get_files_info("calculator", dir)
        if content.startswith("Error:"):
            print(f"\t{content}")
        else:
            print(content)
        print()

test()
