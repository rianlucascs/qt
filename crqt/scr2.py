from utils import PATH
from sys import path
from dataclasses import dataclass
from strats.template import Template
from json import load, dump
from os.path import exists
from os import mkdir

class ListFeatures:
    def __init__(self, number_of_features_in_a_combination=None):
        self.number_of_features_in_a_combination = number_of_features_in_a_combination
        self.path_features_py = f'{path[0]}\\data\\features\\features.py'    
        self.path_combinations_txt = f'{path[0]}\\data\\features\\combinations\\{number_of_features_in_a_combination}\\combinations.txt'


    def reading(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    @property
    def inventory(self):
        """Features disponíveis"""
        file = self.reading(self.path_features_py)
        number = 0
        number_of_features = []
        for row in file.split('\n'):
            if 'def' in row:
                number += 1
                number_of_features.append(int(row.split('(')[0].split(' ')[1].replace('feature', '')))
        return [number, number_of_features]
    
    @property
    def combinations(self):
        number = 3
        number_of_features = [[12, 1], [23, 13], [14, 33]]
        return [number, number_of_features]
    
    def main(self):
        if self.number_of_features_in_a_combination == 1:
            return self.inventory
        
        elif self.number_of_features_in_a_combination >= 2:
            return self.combinations

class FeaturesManagement:

    def __init__(self, ticker, start, end, column='Adj Close', name_model='DecisionTreeClassifier', 
                 config_model={'max_depth': 3, 'criterion': 'gini'}):
        self.list_features = ListFeatures()
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.name_model = name_model
        self.config_model = config_model

        self.name = ticker.upper().split('.')[0]

        self._path_results = f'{path[0]}\\data\\features\\results'
    
    def writing(self, path, message):
        with open(path, 'a', encoding='utf-8') as file:
            file.write(message)
        return None

    def writing_json(self, path, data):
        with open(path, 'w') as file:
            dump(data, file, indent=4)
            
    def create_folders(self, number_of_features_in_a_combination):
        path = f'{self._path_results}\\{self.name}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.start} {self.end}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{self.column}'
        if not exists(path):
            mkdir(path)

        path = f'{path}\\{number_of_features_in_a_combination}'
        if not exists(path):
            mkdir(path)

        _path = f'{path}\\{self.name_model}'
        if not exists(_path):
            mkdir(_path)

        path = f'{_path}\\config_model.json'
        if not exists(path):
            self.writing_json(mkdir(path), self.config_model)
        
        return f'{_path}\\results.json'
    

    def main(self):
        number_of_features = self.list_features.main()
        path_results = self.create_folders(self.number_of_features_in_a_combination)

        results = {}
        for f in number_of_features:
            results[f] = Template(self.ticker, self.start, self.end, [f], self.column, self.name_model, self.config_model).model_result_during_creation[1]
            self.writing_json(path_results, results)

if __name__ == '__main__':
    FeaturesManagement('goau4.sa', '2012-05-15', '2022-05-15').main()

