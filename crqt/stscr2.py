from os import startfile
from os.path import exists
from sys import path
from utils.file import writing

if __name__ == '__main__':
    path_bat = f'{path[0]}\\tools\\bats\\stscr2.bat'
    if not exists(path_bat):
        writing(f'{path[0]}\\tools\\bats\\stscr2.bat',
                f'color 4F\ncls\ncd {path[0]}\npython scr2.py')
    startfile(path_bat)

