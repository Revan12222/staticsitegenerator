import os
import shutil


def copy_dir(source,destination):
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    print(source)
    if not os.path.exists(source):
        raise Exception("Invalid source directory")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    contents = os.listdir(source)
    for content in contents:
        content_path = os.path.join(source,content)
        if os.path.isdir(content_path):
            copy_dir(content_path,os.path.join(destination,content))
        else:
            shutil.copy(content_path,destination)

def create_file_path(destination):
    if os.path.exists(destination):
        return
    directories = destination.split("/")
    file = directories.pop()
    current = "."
    for directory in directories:
        if directory == ".":
            continue
        current += "/directory"
        if os.path.exists(current):
            continue
        else:
            os.mkdir(current)
    with open(destination, "w") as file:
        file.write("")


    
