import os
from langchain.tools import tool


@tool
def list_files(path: str, recursive: bool = False) -> list[str]:
    """
    Return a list of files in the given directory.
    """
    print("\n--- Listing Files ---\n")
    file_list = []
    if recursive:
        for root, dirs, files in os.walk(path):
            for f in files:
                file_list.append(os.path.join(root, f))
    else:
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                file_list.append(f)
    return file_list


@tool
def read_file(filename: str) -> str:
    """
    Return the content of a file as a string.
    """
    print(f"\n--- Reading File {filename} ---\n")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
