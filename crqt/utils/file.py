
from sys import path
from os.path import exists

fpath = lambda fpath: f'{path[0]}\\{fpath}'

def writing(path_, message):

    with open(fpath(path_), 'a', encoding='utf-8') as file:
        file.write(message)
    return None