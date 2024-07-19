
from yfinance import download
from tools.create_list_tickers import TickersMt5
from numpy import where
from sys import path    
from os.path import exists
from os import remove
from pandas import DataFrame
from json import dump

class SetPath:

    def __init__(self):
        self._path = lambda filename: f'{path[0]}\\data\\scr3\\{filename}.json'

    def get(self):
        
        print('[ 1 ] Update')
        print('[ 2 ] New file')
        check = input('...')
        
        if check == '1':
            _path = self._path('metric')
            while True:
                if input('Confirmar exclusão de arquivo digitar "metric.json": ') == 'metric.json':       
                    if exists(_path):
                        remove(_path)
                    break
            return _path
            
        if check == '2':
            return self._path(input('filename: '))
        
        return None
        

class Data:

    def __init__(self, ticker, period):
        self.data = download(ticker, period=period, progress=False)

    def _condition_serie_day_high_or_low(self, data):
        data['high_or_low'] = where(data['Open'] > data['Close'], 'low', 'high')
        data['high_or_low'] = where(data['Open'] == data['Close'], 'null', data['high_or_low'])
        return data
    
    def _calc_serie_difference_extremes(self, data):
        data['amp_sombras'] = where(data['high_or_low'] == 'low',
                                            data['Close'] - data['Low'], data['High'] - data['Open'])
        return data
    
    def _calc_serie_vol_day(self, data):
        data['vol_day'] = data['Close'] - data['Open']
        return data
    
    def get(self):
        data = self._condition_serie_day_high_or_low(self.data)
        data = self._calc_serie_difference_extremes(data)
        data = self._calc_serie_vol_day(data)
        return data

class DicionaryData:

    def __init__(self, ticker, period, data):
        self.ticker = ticker        
        self.period = period
        self.data = data
    
    def get(self):
        return {
            'ticker': self.ticker, 
            'mm_vol_day': self.data['vol_day'].mean(),
            'mm_amp_sombras': self.data['amp_sombras'].mean(), # Não é tão relevante observamos que a amp de dias de baixa é menor em relação aos dias de alta
            'mm_amp_sombras_high_and_low': DataFrame(self.data.groupby('high_or_low').mean())['amp_sombras'].reset_index().values.tolist(),
            '%_d_high_low' : DataFrame(self.data['high_or_low'].value_counts()/len(self.data)).reset_index().values.tolist(),
            'amostra': len(self.data),
            'last_price': self.data['Close'].values[-1],
            'mm_volume': self.data['Volume'].mean(),
            'mm_volume_NTC': '{:.2e}'.format(self.data['Volume'].mean()),
            'std_volume': self.data['Volume'].std(),
            'mm_volume / std_volume': self.data['Volume'].mean() / self.data['Volume'].std(),
            }

class VolatilityCreateData:
    
    def main(self):
        path = SetPath().get()
        periods = ['5y', '4y', '3y', '2y', '1y']
        dic = {}
        pass_ticker = []
        if path != None:
            for period in periods:
                for ticker in TickersMt5().get():
                    if not ticker in pass_ticker:
                        print(period, ticker)
                        try:
                            data = Data(ticker, period).get()
                            dic[f'{period} {ticker}'] = DicionaryData(ticker, period, data).get()
                        except IndexError:
                            if period == '5y':
                                pass_ticker.append(ticker)
                            print(f'\nFailed dic: {ticker}')

            with open(path, 'w') as file:
                dump(dic, file, indent=4)

            print('end.')

if __name__ == '__main__':
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
    VolatilityCreateData().main()