#!/bin/env python3
import os

PAGE_DIR = "./pages/"
TEMPLATE_DIR = "./templates/"
TARGET_DIR = "./docs/"

INCLUDE_MARKER = "&include("
INCLUDE_MARKER_END = ")"

def process_dir(path: str = "") -> None:
    items = os.listdir(PAGE_DIR + path)
    for name in items:
        if os.path.isdir(PAGE_DIR + path + name):
            process_dir(path + name + "/")
        else:
            process_file(path + name)


def process_file(filepath: str) -> str:
    print("processing " + filepath)
    contents = read_file(PAGE_DIR + filepath)
    while INCLUDE_MARKER in contents:
        contents = apply_include(contents)
    
    ensure_dir(TARGET_DIR + filepath)

    with open(TARGET_DIR + filepath, "w") as f:
        f.write(contents)


def ensure_dir(filepath: str):
    i = len(filepath) - filepath[::-1].find("/")
    dir = filepath[:i]
    if not os.path.exists(dir):
        os.mkdir(dir)


def apply_include(contents: str) -> str:
    included_file = get_included_name(contents)
    
    new_contents = read_file(TEMPLATE_DIR + included_file)
    return insert_contents(contents, new_contents)


def insert_contents(contents, new_contents):
    index_start, index_end = get_marker_indices(contents)
    return contents[:index_start] + new_contents + contents[index_end+1:]


def get_included_name(contents):
    marker_start, marker_end = get_marker_indices(contents)
    name_start = marker_start + len(INCLUDE_MARKER)
    name_end = marker_end - len(INCLUDE_MARKER_END)
    return contents[name_start:name_end + 1]


def get_marker_indices(contents: str) -> tuple:
    index_start = contents.find(INCLUDE_MARKER)
    index_end   = contents.find(INCLUDE_MARKER_END, index_start)
    return (index_start, index_end)


def read_file(filepath: str):
    contents = ""
    with open(filepath, "r") as f:
        contents = f.read()
    return contents
    

if __name__ == "__main__":
    process_dir()