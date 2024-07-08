
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

# class ApplyFilter:

#     def _mm_amp_sombras_high_and_low(data):
#         print(data)

class Analysis:

    def processing_data(self, data):
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='low', new_column='mm_amp_sombras_low')
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='high', new_column='mm_amp_sombras_high')
        data = Processing.list_in_df(data, column='mm_amp_sombras_high_and_low', key='null', new_column='mm_amp_sombras_null')
        data['abs_mm_vol_day'] = abs(data['mm_vol_day'])
        return data

    def main_1(self):
        data = GetData('metric', '5y').get()
        data = self.processing_data(data)
        data = FilterMean(data, 'abs_mm_vol_day', above_average=True).Apply()
        data = FilterMean(data, 'mm_volume / std_volume', above_average=True).Apply()
        data = FilterMean(data, 'last_price', above_average=True, set_number=5).Apply()
        print(data[['ticker', 'last_price', 'mm_amp_sombras_null']])
        print(list(data.columns))

if __name__ == '__main__':
    Analysis().main_1()

"""
Mean "abs_mm_vol_day": 0.044391760741945854

Mean "mm_volume / std_volume": 0.6095069644424111
       ticker  last_price  mm_amp_sombras_null   
10   ARZZ3.SA   51.349998             0.299999   
42   BRKM3.SA   18.240000             0.419412   
146  MGLU3.SA   12.050000             0.915221   
165  OIBR3.SA    5.400000             1.182629   
225  VALE3.SA   62.220001             0.508890   
242  AZUL4.SA    7.340000             0.346154   
247  SUZB3.SA   57.009998             0.652222   
264  AMBP3.SA   12.900000             0.274183   
279  CASH3.SA    5.850000             0.326370   
281  AERI3.SA    5.100000             0.574074   
298  ALLD3.SA    7.450000             0.150909   
300  BLAU3.SA   10.490000             0.551429   
336  BHIA3.SA    5.450000             1.521453   

['ticker', 'mm_vol_day', 'mm_amp_sombras', 'mm_amp_sombras_high_and_low', 
'%_d_high_low', 'amostra', 'last_price', 'mm_volume', 'mm_volume_NTC', 
'std_volume', 'mm_volume / std_volume', 'mm_amp_sombras_low', 'mm_amp_sombras_high', 
'mm_amp_sombras_null', 'abs_mm_vol_day']
"""
    