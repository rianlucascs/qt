from warnings import filterwarnings
from dataclasses import dataclass
from data import Market
from numpy import where
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from strats import add
from pandas import concat

filterwarnings('ignore')

@dataclass
class Models:

    name_model: str
    config_model: dict
    data_train: DataFrame

    @property
    def _coef_decision_tree_classifier(self):
        Tree = DecisionTreeClassifier(criterion=self.config_model['criterion'], max_depth=self.config_model['max_depth'])
        Tree.fit(self.data_train[self.data_train.columns[5:].values], self.data_train.alvo_bin)
        return Tree 
    
    def main(self):
        on_models = ['DecisionTreeClassifier'] # < --- !
        if self.name_model in on_models:
            match self.name_model:
                case 'DecisionTreeClassifier':
                    return self._coef_decision_tree_classifier
        else:
            raise TypeError

class Template:
    
    def __init__(self, ticker, start, end, features=[], column='Adj Close', name_model='DecisionTreeClassifier',
                  config_model={'max_depth': 3, 'criterion': 'gini'}):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.features = features
        self.name_model = name_model
        self.config_model = config_model

        self.market_data_train_test = Market(ticker, start, end, column=column).get_price
        self.market_data = Market(ticker, start, column=column).get_price

    def _initial_processing(self, data):
        data['retorno'] = data['adj_close'].pct_change(1)
        data['alvo'] = data['retorno'].shift(-1)
        data['centavos'] = data['adj_close'] - data['adj_close'].shift(1)
        data['alvo_bin'] = where(data['alvo'] > 0, 1, 0)
        data = add.features(self.features, data)
        return data

    def _split_data(self, data):
        train = data[data.index[0]: data.index[round(data.shape[0] * 0.50)]].dropna()
        test = data[data.index[round(data.shape[0] * 0.50)]: data.index[-1]]
        return [train, test]
    
    @property
    def _get_coef(self):
        data = self.market_data_train_test
        data = self._initial_processing(data)
        split_data = self._split_data(data)
        try:
            coef = Models(self.name_model, self.config_model, split_data[0]).main()
        except ValueError:
            return ('', 'ValueError')
        return coef
    
    def _processes_result(self, data):
        data = concat([data[0], data[1]], axis=0) if type(data) == list else data
        data['serie_retorno'] = where(data['previsto'] == 1, data['centavos'], '0')
        data['serie_retorno'] = where(data['previsto'] == 0, -1 * data['centavos'], data['serie_retorno']).astype(float)
        data['retorno_modelo'] = data['serie_retorno'].cumsum() * 100
        return data

    def _percentage_positive_days(self, data):
        return (data['serie_retorno'] > 0).value_counts()[True] / len(data)
    
    def _percentage_positive_days_test(self, data):
        return (data[0]['serie_retorno'] > 0).value_counts()[True] / len(data[0])
    
    def _lost_data(self, data, _data):
        return len(data) - len(_data)

    def _correct_signal(self, data):
        try:
            if data[0] == 'error':
                pass
        except:
            data[0] = 0
        try:
            if data[1] == 'error':
                pass
        except:
            data[1] = 0
        return data
    
    def _number_of_signals(self, data, n=0): # n = 0 or 1
        if n != None:
            form = lambda n: list(self._correct_signal(DataFrame(data[n]['previsto']).value_counts()))
            return form(n)
        else:
            form = list(self._correct_signal(DataFrame(data['previsto']).value_counts()))
            return form

    def _overfitting(self, x, y):
        return abs(x - y)
    
    def _mean_serie_retorno(self, data):
        return data['serie_retorno'].mean()
    
    def _std_serie_retorno(self, data):
        return data['serie_retorno'].std()

    def _metric_result_during_creation(self, data, _data):
        __data = self._split_data(data)
        return [
            x:= accuracy_score(__data[0]['alvo_bin'], __data[0]['previsto']) * 100,
            y:= accuracy_score(__data[1]['alvo_bin'], __data[1]['previsto']) * 100,
            self._percentage_positive_days(data),
            self._percentage_positive_days_test(__data),
            self._lost_data(data, _data),
            self._number_of_signals(__data, 0), 
            self._number_of_signals(__data, 1),
            self._number_of_signals(data, None),
            self._overfitting(x, y),
            self._mean_serie_retorno(data),
            self._std_serie_retorno(data)
        ]
    
    @property
    def model_result_during_creation(self):
        _data = self.market_data_train_test
        data = self._initial_processing(_data)
        split_data = self._split_data(data)
        coef = self._get_coef
        if type(coef) == tuple:
            return coef
        predict_train = coef.predict(split_data[0][split_data[0].columns[5:]])
        predict_test = coef.predict(split_data[1][split_data[1].columns[5:]])
        split_data[0]['previsto'] = predict_train
        split_data[1]['previsto'] = predict_test
        data = self._processes_result(split_data)
        metric = self._metric_result_during_creation(data, _data)
        return [data, metric]
    
    def metric_result_model_after_creation(self, data):
        """Metricas referentes aos resultados pós treino"""
        return [
            self._number_of_signals(data, None),
            self._mean_serie_retorno(data),
            self._std_serie_retorno(data)
        ]

    @property
    def result_model_after_creation(self):
        data = self.market_data
        data = self._initial_processing(data)
        coef = self._get_coef
        if type(coef) == tuple:
            return coef
        data['previsto'] = coef.predict(data[data.columns[5:]])
        data = self._processes_result(data)
        _data = data[len(self.market_data_train_test):]
        metric = self.metric_result_model_after_creation(_data)
        return [data, metric]