from utils import PATH
from sys import path
from dataclasses import dataclass
from strats.template import Template
from json import load, dump
from os.path import exists
from os import mkdir

class ListFeatures:
    def __init__(self, features=None):
        if self.check_list(features):
            self.number_of_features_in_a_combination = len(features[0])
        else:
            self.number_of_features_in_a_combination = 1
        self.path_combinations_txt = f'{path[0]}\\data\\features\\combinations\\{self.number_of_features_in_a_combination}\\combinations.txt'  

    def check_list(self, features): # if list[list]
        if all(isinstance(elem, list) for elem in features):
            return True
        return False

    def number(self):
        return self.number_of_features_in_a_combination

class FeaturesManagement:

    def __init__(self, ticker, start, end, column='Adj Close', name_model='DecisionTreeClassifier', 
                 config_model={'max_depth': 3, 'criterion': 'gini'}, features=[]):
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

    def create_folders(self):
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
        path = self.create_folders()
        try:
            file = self.reading_txt(path)
        except FileNotFoundError:
            pass

        for f in self.features:
            if not all(isinstance(elem, list) for elem in self.features):
                f = [f]
            metric = Template(self.ticker, self.start, self.end, f, self.column, self.name_model, self.config_model).model_result_during_creation[1]
            message = f'%{f}% {metric}\n'
            try:
                if not f'%{f}%' in file:
                    self.writing_txt(path, message)
            except:
                self.writing_txt(path, message)
   
if __name__ == '__main__':
    FeaturesManagement(
        ticker='azul4.sa', 
        start='2012-05-15', 
        end='2022-05-15',
        features=[[1, 2], [3, 4]]
        ).main()

