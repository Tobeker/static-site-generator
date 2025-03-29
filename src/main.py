import shutil
import os
import sys
from pathlib import Path
from blocktype import *

def copy_directory(path, destination):
    lst = os.listdir(path)
    for l in lst:
        l_path = os.path.join(path, l)
        l_destination = os.path.join(destination, l)
        if os.path.isfile(l_path):
            shutil.copy(l_path, l_destination)
        else:
            os.mkdir(l_destination)
            copy_directory(l_path, l_destination)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file2:
        template = file2.read()
    
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(html_string)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as destination:
        destination.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def main():
    if len(sys.argv[1]) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    #alten public ordner löschen, wenn einer existiert
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    #neuen public ordner erstellen
    os.mkdir("docs")
    destination = "docs"
    #static verzeichnis kopieren
    if os.path.exists("static/"):
        path = "static/"
        copy_directory(path, destination)
    else:
        raise Exception("no static/ directory")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()