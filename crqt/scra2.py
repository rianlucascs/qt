
from json import load
from sys import path
from pandas import DataFrame
from utils.filter_mean import FilterMean


__processing_data__ = 'scr3.py'

class GetData:
    
    def __init__(self, filename='metric', filter='5y'):
        self.filename = filename
        self.filter = filter

    def load_data(self):
        with open(f'{path[0]}\\data\\scr3\\{self.filename}.json') as file:
            return load(file)

    def select_key(self, _load_data, filter):
        return [key for key in _load_data.keys() if filter in key]

    def dic_in_serie(self, data, keys):
        return [data[key] for key in keys]

    def get(self):
        data = self.load_data()
        keys = self.select_key(data, self.filter)
        data = self.dic_in_serie(data, keys)
        data = DataFrame(data)
        return data

class Processing:

    @staticmethod
    def list_in_df(data, column='mm_amp_sombras_high_and_low', key='low', new_column='mm_amp_sombras_low'):
        lis = []
        for row in data[column].values:
            row = [item for item in row if key in item]
            if not(len(row)):
                row = 0
            else:
                row = row[0][1]
            lis.append(row)
        data[new_column] = lis
        return data

class Analysis:

    def processing_data(self, data):
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='low', new_column='mm_amp_sombras_low')
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='high', new_column='mm_amp_sombras_high')
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='null', new_column='mm_amp_sombras_null')
        data = Processing.list_in_df(data, column='%_d_high_low', key='low', new_column='%_d_low')
        data = Processing.list_in_df(data, column='%_d_high_low', key='high', new_column='%_d_high')
        data = Processing.list_in_df(data, column='%_d_high_low', key='null', new_column='%_d_null')
        data['abs_mm_vol_day'] = abs(data['mm_vol_day'])
        return data

    def main_1(self):
        data = GetData('metric', '1y').get()
        data = self.processing_data(data)
        data = FilterMean(data, 'abs_mm_vol_day', above_average=True).Apply()
        data = FilterMean(data, 'mm_volume / std_volume', above_average=True).Apply()
        data = FilterMean(data, 'last_price', above_average=True, set_number=5).Apply()
        print(data[['ticker', 'last_price', 'mm_vol_day', 'amostra', '%_d_low', '%_d_high', '%_d_null']])
        print(list(data.columns))

if __name__ == '__main__':

    """

    # Objetivo

    - Definir os melhores ativos para criar estratégias e alocar capital
    - Refinar estratégias durante a criação com base nas características do ativo

    """

    Analysis().main_1()

"""
Mean "abs_mm_vol_day": 0.044391760741945854

       ticker  last_price  mm_vol_day  amostra   %_d_low  %_d_high  %_d_null
10   ARZZ3.SA   51.349998   -0.177530      251  0.565737  0.430279  0.003984 #
39   BRAP3.SA   17.950001   -0.046335      251  0.589641  0.390438  0.019920 ~
40   BRAP4.SA   18.510000   -0.039044      251  0.541833  0.418327  0.039841
41   BRFS3.SA   22.670000    0.046892      251  0.466135  0.509960  0.023904
68   CSAN3.SA   13.540000   -0.038566      251  0.529880  0.446215  0.023904
90   EMBR3.SA   36.150002    0.052351      251  0.458167  0.537849  0.003984 <
110  GGBR3.SA   16.350000   -0.041574      251  0.557769  0.418327  0.023904
123  HYPE3.SA   28.700001   -0.054582      251  0.545817  0.442231  0.011952 #
127  JBSS3.SA   32.270000    0.048725      251  0.478088  0.494024  0.027888
135  LEVE3.SA   32.340000   -0.047999      251  0.513944  0.462151  0.023904
146  MGLU3.SA   12.050000   -0.124132      251  0.581673  0.374502  0.043825
169  PETR3.SA   40.380001    0.038366      251  0.490040  0.505976  0.003984
170  PETR4.SA   38.049999    0.039522      251  0.434263  0.549801  0.015936
188  RENT3.SA   42.000000   -0.122580      251  0.545817  0.446215  0.007968 Variaveis não compatives
191  ROMI3.SA   10.470000   -0.035720      251  0.585657  0.386454  0.027888 Variaveis não compatives
225  VALE3.SA   62.220001   -0.075298      251  0.565737  0.426295  0.007968
236  PRIO3.SA   43.759998   -0.044423      251  0.521912  0.478088  0.000000
242  AZUL4.SA    7.340000   -0.088685      251  0.613546  0.382470  0.003984 #
255  YDUQ3.SA   10.410000   -0.040876      251  0.537849  0.450199  0.011952
264  AMBP3.SA   12.900000   -0.036037      251  0.573705  0.414343  0.011952
281  AERI3.SA    5.100000   -0.102709      251  0.565737  0.294821  0.139442
300  BLAU3.SA   10.490000   -0.051315      251  0.589641  0.406375  0.003984
304  RECV3.SA   18.540001   -0.042749      251  0.533865  0.454183  0.011952
336  BHIA3.SA    5.450000   -0.143195      251  0.561753  0.386454  0.051793 

['ticker', 'mm_vol_day', 'mm_amp_sombras', 'mm_amp_sombras_high_and_low', 
'%_d_high_low', 'amostra', 'last_price', 'mm_volume', 'mm_volume_NTC', 
'std_volume', 'mm_volume / std_volume', 'mm_amp_sombras_low', 'mm_amp_sombras_high', 
'mm_amp_sombras_null', 'abs_mm_vol_day']
"""
    