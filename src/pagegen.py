import os
import shutil

from textnode import markdown_to_html_node
from textnode import extract_title
from copydir import create_file_path

def generate_page(from_path,template_path,dest_path,basepath):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        contents = file.read()
    with open(template_path) as file:
        template = file.read()
    contents_html = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}",contents_html)
    template = template.replace("href=\"/",f"href=\"{basepath}")
    template = template.replace("src=\"/",f"src=\"{basepath}")
    create_file_path(dest_path)
    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content,template_path,dest_dir_path,basepath):
    contents = os.listdir(dir_path_content)
    print(contents)
    if not contents:
        return
    for content in contents:
        full_source_path = os.path.join(dir_path_content,content)
        full_dest_path = os.path.join(dest_dir_path,content)
        if os.path.isdir(full_source_path):
            os.mkdir(full_dest_path)
            generate_pages_recursive(full_source_path,template_path,full_dest_path,basepath)
        elif content.endswith(".md"):
            generate_page(full_source_path,template_path,full_dest_path.replace(".md",".html"),basepath)
        else:
            shutil.copy(full_source_path,full_dest_path)