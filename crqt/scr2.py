"""
# scr2

# Descrição

- Gerar combinações de features 
- Armazenar a metrica do treinamento e o teste do modelo
- Sistema padronizado de diretórios e arquivos

# Ojetivo

- Encontrar combinações de 2 features para iniciar o processo de otimização
- encontrar as melhores features iniciais para cada ativo

# Obs

- Não é feito mais de 2 combinações pq a partir de 3 elementos a quantidade
- de combinações possíveis é elta.

# Combinações Possíveis em Relação ao Número de Elementos (1 a 158)

2   | 12,403        | Doze Mil, Quatrocentos E Três
3   | 644,956       | Seiscentos E Quarenta E Quatro Mil, Novecentos E Cinquenta E Seis
4   | 24,992,045    | Vinte E Quatro Milhões, Novecentos E Noventa E Dois Mil E Quarenta E Cinco
5   | 769,754,986   | Setecentos E Sessenta E Nove Milhões, Setecentos E Cinquenta E Quatro Mil, Novecentos E Oite

"""

from utils import PATH
from sys import path
from strats.template import Template
from json import load, dump
from os.path import exists
from os import mkdir
from math import comb
from itertools import combinations_with_replacement
from sys import stdout
from num2words import num2words
from yfinance import download

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
        self._path_results = f'{path[0]}\\data\\scr2'
        self.name_config_model = ' '.join(list(map(str, config_model.values())))

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

        path = f'{path}\\{self.name_model}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.name_config_model}'
        if not exists(path):
            mkdir(path)

        return f'{path}\\results.txt'
    
    def main(self):
        path = self.create_folders_results()
        try:
            file = self.reading_txt(path)
        except FileNotFoundError:
            file = None

        metric = lambda f: Template(self.ticker, self.start, self.end, f, self.column, self.name_model, self.config_model).model_result_during_creation[1]
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

    def message():
        print(20*'\n'+f'# Combinações Possíveis em Relação ao Número de Elementos (1 a {len(inventory_features())+1})\n')
        for k in range(2, 6):
            c = number_of_combinations(k=k)
            print(f'{k}'.ljust(3), '|', f'{c:,.0f}'.ljust(13), '|', num2words(c, lang='pt_BR').title())
        print()

def start_date_ticker(ticker):
    data = download(ticker, period='max', progress=False)
    return str(data.index[0])[:10]

if __name__ == '__main__':

    """
    Cria combinações com as features disponíveis
    """
    CombinationsByElementQuantity.message()

    k = 2
    ticker = 'arzz3.sa'

    # start = start_date_ticker(ticker)
    start = '2013-06-15'
    end='2023-06-15'

    # features=inventory_features()
    features=combinations_in_rane(k=k)

    FeaturesManagement(
        ticker=ticker, 
        start=start,
        end=end,
        features=features
        ).main()