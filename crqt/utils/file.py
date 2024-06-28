
from os import remove
from os.path import exists

def writing(path, content, update=False):
    if exists(path) and update:
        remove(path)
    with open((path), 'a', encoding='utf-8') as file:
        file.write(content)
    return None

def read(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()