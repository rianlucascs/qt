"""
# scr2

- Armazenar a metrica do treinamento e o teste do modelo
- Gerar combinações de features 
- Sistema padronizado de diretórios e arquivos

"""

from utils import PATH
from sys import path
from dataclasses import dataclass
from strats.template import Template
from json import load, dump
from os.path import exists
from os import mkdir
from math import comb
from itertools import combinations_with_replacement
from sys import stdout
from num2words import num2words

class ListFeatures:
    def __init__(self, features=None):
        if  features != None:
            if self.check_list(features):
                self.number_of_features_in_a_combination = len(features[0])
            else:
                self.number_of_features_in_a_combination = 1

    def check_list(self, features): # if list[list]
        if all(isinstance(elem, list) for elem in features):
            return True
        return False

    def number(self):
        return self.number_of_features_in_a_combination

class FeaturesManagement:
    
    def __init__(self, ticker, start, end, column='Adj Close', name_model='DecisionTreeClassifier', 
                 config_model={'max_depth': 3, 'criterion': 'gini'}, features=None):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.name_model = name_model
        self.config_model = config_model
        self.features = features
        self.list_features = ListFeatures(features).number()
        self.name = ticker.upper().split('.')[0]
        self._path_results = f'{path[0]}\\data\\features\\results'

    def writing_json(self, path, data):
        with open(path, 'a') as file:
            dump(data, file, indent=4)

    def reading_json(self, path):
        with open(path, 'r') as file:
            return load(file)

    def writing_txt(self, path, message):
        with open(path, 'a', encoding='utf-8') as file:
            file.write(message)
        return None
    
    def reading_txt(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def create_folders_results(self):
        path = f'{self._path_results}\\{self.name}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.start} {self.end}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.column}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.list_features}' # rabge combination
        if not exists(path):
            mkdir(path)

        _path = f'{path}\\{self.name_model}'
        if not exists(_path):
            mkdir(_path)

        path = f'{_path}\\config_model.json'
        if not exists(path):
            self.writing_json(path, self.config_model)

        return f'{_path}\\results.txt'
    
    def main(self):
        path = self.create_folders_results()
        try:
            file = self.reading_txt(path)
        except FileNotFoundError:
            file = None

        metric = lambda f: Template(self.ticker, self.start, self.end, f, self.column, self.name_model, self.config_model).model_result_during_creation[1]
        s = lambda x: x.replace(',', '.')
        for i, f in enumerate(self.features):
            stdout.write('\r' + f'{i:,.0f} / {len(self.features):,.0f}')
            if not all(isinstance(elem, list) for elem in self.features):
                f = [f]
            if file != None:
                if not f'%{f}%' in file:
                    message = f'%{f}% {metric(f)}\n'
                    self.writing_txt(path, message)
            else:
                message = f'%{f}% {metric(f)}\n'
                self.writing_txt(path, message)

def inventory_features():
    """Features disponíveis"""
    path_features = f'{path[0]}\\data\\features\\features.py'
    list_features = []
    with open(path_features, 'r', encoding='utf-8') as file:
        file = file.read().split('\n')
        for row in file:
            if 'def' in row:
                list_features.append(int(row.split('(')[0].split(' ')[1].replace('feature', '')))
    return list_features

def number_of_combinations(n=None, k=2):
    n = len(inventory_features()) + 1 if n == None else n
    return comb(n, k)

def combinations_in_rane(k, x=None, y=None):
    """n=elementos, x=start, y=end"""
    if k < 1:
        raise ValueError
    if (x != None) and (y != None) and (x > y) and (x > 0):
        raise ValueError
    numbers = list(range(1, len(inventory_features()) + 1)) if (x == None) and (y == None) else list(range(x, y+1))
    all_combinations = list(combinations_with_replacement(numbers, k))
    all_combinations = [list(t) for t in all_combinations]
    return all_combinations

class CombinationsByElementQuantity:
    print(20*'\n'+f'# Combinações Possíveis em Relação ao Número de Elementos (1 a {len(inventory_features())+1})\n')
    for k in range(2, 6):
        c = number_of_combinations(k=k)
        print(f'{k}'.ljust(3), '|', f'{c:,.0f}'.ljust(13), '|', num2words(c, lang='pt_BR').title())
    print()

if __name__ == '__main__':
    CombinationsByElementQuantity
    FeaturesManagement(
        ticker='goau4.sa', 
        start='2012-05-15', 
        end='2022-05-15',
        # features=inventory_features()
        # features=[[22, 12]]
        features=combinations_in_rane(k=2)
        ).main()