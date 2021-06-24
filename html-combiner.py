#!/bin/env python3
import os

PAGE_DIR = "./pages/"
TEMPLATE_DIR = "./templates/"
TARGET_DIR = "./docs/"

INCLUDE_DECORATOR = "&include("
INCLUDE_DECORATOR_END = ")"

def process_dir(path: str = "") -> None:
    items = os.listdir(PAGE_DIR + path)
    for i in items:
        i_path = path + i
        if os.path.isdir(i_path):
            process_dir(i_path + "/")
        else:
            process_file(i_path)


def process_file(filepath: str) -> str:
    contents = read_file(PAGE_DIR, filepath)
    while INCLUDE_DECORATOR in contents:
        contents = replace_next_include(contents)
    
    with open(TARGET_DIR + filepath, "w") as f:
        f.write(contents)


def replace_next_include(contents: str) -> str:
    index_start, index_end = get_include_indices(contents)

    include_name = contents[index_start + len(INCLUDE_DECORATOR):index_end]
    
    new_contents = read_file(TEMPLATE_DIR, include_name)
    return contents[:index_start] + new_contents + contents[index_end+1:]


def get_include_indices(contents: str) -> tuple:
    index_start = contents.find(INCLUDE_DECORATOR)
    index_end   = contents.find(INCLUDE_DECORATOR_END, index_start)
    return (index_start, index_end)


def read_file(folder: str, filepath: str):
    contents = ""
    with open(folder + filepath, "r") as f:
        contents = f.read()
    return contents
    


if __name__ == "__main__":
    process_dir()