from utils import complex_writing, add_path

folder = 'features'
file = 'add_feature.py'

_import_features = 'import features.features as ft'

def __init__(start=1, end=1000):
    _path = add_path([folder, file])
    complex_writing(_path, f'{_import_features}\n', True, True)
    complex_writing(_path, 'def __init__(vars, df_data, retorno):', False, True)
    
    numbers = list(range(start, end + 1))
    for number in numbers:
        complex_writing(_path,
            f'    if {number} in vars:\n        df_data["f{number}"] = ft.feature{number}(retorno)\n')
    complex_writing(_path, '    return df_data')

if __name__ == '__main__':
    __init__(start=1, end=5000)