
from dataclasses import dataclass
from data.data import Market
from numpy import where
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier

@dataclass
class Models:

    name_model: str
    config_model: dict
    data_train: DataFrame

    @property
    def _coef_decision_tree_classifier(self):
        Tree = DecisionTreeClassifier(criterion='gini', max_depth=self.config['max_depth'])
        Tree.fit(self.data_train[self.data_train.columns[5:].values], self.data_train.alvo_bin)
        return Tree 
    
    def main(self):
        on_models = ['DecisionTreeClassifier']
        if self.name_model in on_models:
            match self.name_model:
                case 'DecisionTreeClassifier':
                    return self._coef_decision_tree_classifier

        else:
            raise TypeError

class Template:
    

    def __init__(self, ticker, start, end, column='Adj Close', features=[], name_model='DecisionTreeClassifier',
                  config_model={'max_depth': 3}):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.features = features
        self.name_model = name_model
        self.config_model = config_model

        self.market_data_train_test = Market(ticker, start, end, column=column).get_price
        self.market_data = Market(ticker, start, column=column).get_price

    def _initial_processing(data):
        data['retorno'] = data['adj_close'].pct_change(1)
        data['alvo'] = data['retorno'].shift(-1)
        data['centavos'] = data['adj_close'] - data['adj_close'].shift(1)
        data['alvo_bin'] = where(data['alvo'] > 0, 1, 0)
        return data

    def _split_data(data):
        train = data[data.index[0]: data.index[round(data.shape[0] * 0.50)]].dropna()
        test = data[data.index[round(data.shape[0] * 0.50)]: data.index[-1]]
        return [train, test]
    
    @property
    def _get_coef(self):
        data = self.market_data_train_test
        data = self._initial_processing(data)
        split_data = self._split_data(data)
        coef = Models(self.name_model, self.config_model, split_data[0]).main()
        return coef
    
    @property
    def model_result_during_creation(self):
        coef = self._get_coef

    @property
    def result_model_after_creation(self):
        pass