from sys import path
from os import remove
from os.path import exists

PATH = path[0].replace('\\tools', '') + '\\strats\\add.py'

def writing(message):
    with open(PATH, 'a', encoding='utf-8') as file:
        file.write(message)
    return None

def main(start=1, end=1000):
    if exists(PATH):
        remove(PATH)
    writing('import features.features as ft\n')
    writing('def features(vars, data):\n')
    numbers = list(range(start, end + 1))
    for number in numbers:
        writing(
            f'    if {number} in vars:\n        data["f{number}"] = ft.feature{number}(data["retorno"])\n')
    writing('    return data')

if __name__ == '__main__':
    main(start=1, end=5000)