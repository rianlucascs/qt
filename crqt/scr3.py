

"""
# scr3

# Descrição

- Loop em todas as ações a vista da bolsa
- Download série ativo
- Aplica regras e retorna métricas para filtro 

# Objetivo

- Criar metricas para avaliação da volatilidade,
- amplitude dos movimentos diários e refinar estratégias
- com base no comportamento predominante do ativo
 
"""

from yfinance import download
from tools.create_list_tickers import TickersMt5
from numpy import where
from utils.file import writing
from sys import path    
from os.path import exists

class ConditionsAndCalculations:

    def __init__(self, data):
        self.data = data

    def _condition_serie_day_high_or_low(self, data):
        data['high_or_low'] = where(data['Open'] > data['Close'], 'low', 'high')
        data['high_or_low'] = where(data['Open'] == data['Close'], 'null', data['high_or_low'])
        return data
    
    def _calc_serie_difference_extremes(self, data):
        data['difference_extremes'] = where(data['high_or_low'] == 'low',
                                            data['Close'] - data['Low'], data['High'] - data['Open'])
        return data
    
    def _calc_serie_vol_day(self, data):
        data['vol_day'] = data['Close'] - data['Open']
        return data

    def _last_processing(self, data):
        from pandas import DataFrame
        return [
            data['vol_day'].mean(),
            data['difference_extremes'].mean(),
            DataFrame(data.groupby('high_or_low').mean())['difference_extremes'].reset_index().values.tolist(),
            DataFrame(data['high_or_low'].value_counts()/len(data)).reset_index().values.tolist(),
            len(data),
        ]

    def main(self):
        data = self.data
        data = self._condition_serie_day_high_or_low(data)
        data = self._calc_serie_difference_extremes(data)
        data = self._calc_serie_vol_day(data)
        data = self._last_processing(data)
        return data
    
class VolatilityCreateData:

    def data(self, ticker):
        return download(ticker, period='5y', progress=False)
    
    def create_data(self):
        _path = f'{path[0]}\\data\\volatility_create_data\\cacls.txt'
        if not exists(_path):
            for ticker in TickersMt5().get():
                data = self.data(ticker)
                cond_calc = ConditionsAndCalculations(data).main()
                if cond_calc[-1] != 0 and cond_calc[1] != 0:
                    _path = f'{path[0]}\\data\\volatility_create_data\\cacls.txt'    
                    writing(_path, str([ticker] + cond_calc) + '\n')
        else:
            print(f'manual remove: {_path}')

    def test(self):
        for ticker in TickersMt5().get():
            data = self.data(ticker)
            cond_calc = ConditionsAndCalculations(data).main()
            print(cond_calc)
            break

if __name__ == '__main__':
    VolatilityCreateData().create_data()