from sys import path

CRQT_FOLDERS = [
    'utils', 
    'communication',
    'utils',
    'data'
    ]

[path.append(f'{path[0]}\\{name}') for name in CRQT_FOLDERS]