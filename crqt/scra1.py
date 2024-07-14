"""
# scra1

# Descrição

- Processa dados criados pelo scr2

# Objetivo

- Filtrar combinações iniciais de features
 
"""

from warnings import filterwarnings
from sys import path
from pandas import DataFrame

filterwarnings('ignore')

__processing_data__ = 'scr2.py'

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
        return f'{path[0]}\\data\\scr2\\{name}\\{date}\\{self.column}\\{self.k}\\{self.name_model}\\{name_config_model}\\results.txt'
 
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

    def df(self):
        df = DataFrame(self.read_data(), columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12'])
        return df
    
class Filters:
    


    @staticmethod
    def A(data):
        lis_index_1 = []
        for col in [7, 8, 9]:
            for index, row_col in data[['index', f'Column{col}']].values:
                if (row_col[0] >= ((row_col[0] + row_col[1]) * (1/3))) and (row_col[1] >= ((row_col[0] + row_col[1]) * (1/3))):
                    lis_index_1.append(index)
        lis_index_2 = []
        for index in lis_index_1:
            if lis_index_1.count(index) == 3:
                if not index in lis_index_2:
                    lis_index_2.append(index)
        data = data[data['index'].apply(lambda x: x in lis_index_2)]
        print(f'Qtd.Data (A): {len(data)}')
        return data
    
    def B(data):
        data['Column10'] = data[['Column10']].astype(float)
        data = data.query('Column10 <= 3')
        print(f'Qtd.Data (B): {len(data)}')
        return data
    
    def C(data):
        data['Column11'] = data[['Column11']].astype(float)
        data = data.query(f'Column11 > 0')
        print(f'Qtd.Data (C): {len(data)}')
        return data
    
    def D(data):
        data = data.query(f'Column11 > {data.Column11.mean()}')
        print(f'Qtd.Data (D): {len(data)}')
        return data
    
    def E(data):
        data['Column5'] = data[['Column5']].astype(float)
        data = data.query(f'Column5 > {data.Column5.mean()}')
        data = data.sort_values(by='Column5')
        print(f'Qtd.Data (E): {len(data)}')
        return data

class Analysis(GetData):

    def main(self):
        data = GetData(self.ticker, self.start, self.end, self.column, self.k).df().reset_index()
        data = Filters.A(data)  
        data = Filters.B(data)
        data = Filters.C(data)
        data = Filters.D(data)
        data = Filters.E(data)
        print(data[['index', 'Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6']])
        print(list(data.columns))
        return data

if __name__ == '__main__':     

    ticker = 'arzz3.sa'
    start = '2013-06-15'
    end='2023-06-15'
    column = 'Adj Close'

    data = Analysis(ticker, start=start, end=end, column=column, k=2).main()


"""
Qtd.Data (A): 1761
Qtd.Data (B): 360
Qtd.Data (C): 62
Qtd.Data (D): 31
Qtd.Data (E): 15

       index    Column1    Column2    Column3   Column4   Column5  Column6
8422    8422   [69, 93]  55.169418  53.258036  0.569318  0.571677     -183
8423    8423   [69, 94]  55.169418  53.258036  0.569318  0.571677     -183
8510    8510   [70, 93]  55.169418  53.258036  0.569318  0.571677     -183
8511    8511   [70, 94]  55.169418  53.258036  0.569318  0.571677     -183
10294  10294  [93, 129]  55.082537  52.389227  0.572794  0.572546     -183
10358  10358  [94, 129]  55.082537  52.389227  0.572794  0.572546     -183
2327    2327   [16, 93]  54.908775  52.562989  0.574098  0.574283     -183
2328    2328   [16, 94]  54.908775  52.562989  0.574098  0.574283     -183
7187    7187   [56, 93]  54.561251  52.215465  0.575402  0.576021     -183
7188    7188   [56, 94]  54.561251  52.215465  0.575402  0.576021     -183
10295  10295  [93, 130]  54.648132  52.128584  0.576271  0.578627     -183
10359  10359  [94, 130]  54.648132  52.128584  0.576271  0.578627     -183
6656    6656   [51, 82]  53.056027  51.231946  0.592608  0.583192     -130
6762    6762   [52, 82]  52.886248  51.401869  0.591759  0.583192     -130
1678    1678   [12, 18]  54.995871  53.140496  0.591736  0.587944      -64

['index', 'Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 
'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12']
"""