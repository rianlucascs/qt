
from warnings import filterwarnings
from sys import path
from pandas import DataFrame

filterwarnings('ignore')

__processing_data__ = 'scr2'

class DataTransformer:
    
    def _data_frame(data):
        df = DataFrame(data, columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12'])
        return df

    def filter1(data):

        # Se sianis Buy e Sell >= 0.3 do total de sinais
        calc = lambda x: (x[0] >= ((x[0] + x[1]) * (1/3))) and (x[1] >= ((x[0] + x[1]) * (1/3)))
        for c in [7, 8, 9]:
            data[f'Column_Filt{c}'] = data[f'Column{c}'].apply(calc)
            data = data[data[f'Column_Filt{c}'] == True]
        return data
    
    def filter2(data):

        # Se overfitting < 3
        data = data[data['Column10'] <= 3]

        # Se média serie retorno > média da média serie retorno * 2
        data = data[data['Column11'] >= (data['Column11'].mean() * 2.2)]

        return data
        # return data


class GetData:

    def __init__(self, ticker, start, end, column='Adj Close', k=2, name_model='DecisionTreeClassifier', 
                 config_model={'max_depth': 3, 'criterion': 'gini'}):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.k = k
        self.name_model = name_model
        self.config_model = config_model
        self.data = None
    
    @property
    def get_path(self):
        name = self.ticker.split('.')[0].upper()
        name_config_model = ' '.join(list(map(str, self.config_model.values())))
        date = f'{self.start} {self.end}'
        return f'{path[0]}\\data\\features\\results\\{name}\\{date}\\{self.column}\\{self.k}\\{self.name_model}\\{name_config_model}\\results.txt'
 
    def read_data(self):
        if self.data is None:
            self.data = []
            with open(self.get_path, 'r', encoding='utf-8') as file:
                file = file.read().split('\n')
                for row in file:
                    if row == '':
                        break
                    f = list(map(int,row.split('% ')[0][2:][:-1].split(', ')))
                    metrics = [f] + eval(row.split('% ')[1])
                    self.data.append(metrics)
        return self.data
    
    @property
    def filter1(self):
        data = self.read_data()
        data = DataTransformer._data_frame(data)
        data = DataTransformer.filter1(data)
        data = DataTransformer.filter2(data)
        return data

if __name__ == '__main__':     

    """
    >>> Processa dados de src2

    """

    ticker = 'azul4.sa' 
    start = '2017-04-11'
    end = '2023-06-15'
    column = 'Adj Close'

    data = GetData(
        ticker, 
        start=start,
        end=end, 
        column=column, 
        k=2, 
        ).filter1

    print(data)

