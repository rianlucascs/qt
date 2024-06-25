
from sys import path
from yfinance import download
from datetime import date, datetime, timedelta
from os.path import exists
from os import mkdir
from pandas import DataFrame, to_datetime

class Market:

    def __init__(self, ticker='', start=None, end=None, column='Adj Close', period='1y', progress=False):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.period = period
        self.progress = progress
        self.column_replace = column.replace(' ', '_').lower()
        self.name = ticker.upper().split('.')[0]
        self.PATH = lambda archive='': f'{path[0]}\\data\\prices\\{self.name}{archive}'

    @property
    def _interval_initial_date(self):
        year = 365
        periods = {'1y': year, '2y': year*2, '3y': year*3, '4y':year*4, '5y':year*5}
        interval_initial = datetime.now() - timedelta(days=periods[self.period])
        return interval_initial

    def _rename_data(self, data):
        data = data.rename(columns={self.column: self.column_replace})
        return data
    
    def _get_price_yfinance(self, bool_data=False, bool_name=False):

        if self.start != None and self.end != None:
            if bool_data:
                data = download(self.ticker, self.start, self.end, progress=False)[[self.column]]
                return self._rename_data(data)
            
            if bool_name:
                name = f'{self.column_replace} {self.start} {self.end}.txt'
                return name

        if self.start != None and self.end == None:
            if bool_data:
                data = download(self.ticker, self.start, str(date.today()), progress=False)[[self.column]]
                return self._rename_data(data)
            
            if bool_name:
                name = f'{self.column_replace} {self.start} {str(date.today())}.txt'
                return name
            
        if self.start == None and self.end == None:
            if bool_data:
                data = download(self.ticker, period=self.period, progress=False)[[self.column]]
                return self._rename_data(data)
            
            if bool_name:
                name = f'{self.column_replace} {str(self._interval_initial_date)[:10]} {str(date.today())}.txt'
                return name

        return None

    @property
    def _create_folder_ticker(self):
        if not exists(self.PATH()):
            mkdir(self.PATH())
        return None

    def _check_exists_file(self, file):
        _ = self._create_folder_ticker
        if exists(self.PATH(f'\\{file}')):
            return True
        return False

    def _message_data(self, data):
        data = data.reset_index().values
        message = ''
        for row in data:
            message += f'{str(row[0])[:10]} {row[1]}\n'
        return message
    
    def _writhing_data(self, data, name):
        message = self._message_data(data)
        with open(self.PATH(f'\\{name}'), 'a', encoding='utf-8') as file:
            file.write(message)
        return None 

    def _reading_data(self, name):
        data = [[], []]
        with open(self.PATH(f'\\{name}'), 'r', encoding='utf-8') as file:
            file = file.read().split('\n')
            for row in file:
                row = row.split(' ')
                try:
                    data[0].append(row[0])
                    data[1].append(row[1])
                except IndexError:
                    pass
        data = DataFrame(data, index=['Date', self.column_replace]).T
        return data

    def _adjust_values(self, data):
        data['Date'] = to_datetime(data['Date'])
        data[self.column_replace] = data[self.column_replace].astype(float)
        data = data.dropna()
        data = data.set_index('Date')
        return data

    @property
    def get_price(self):
        """
        >>> Se o cache não existir então escrita e retornar yfinance 
        >>> Se existir então leitura e retornar a leitura
        """
        name = self._get_price_yfinance(bool_name=True)
        if not self._check_exists_file(name):
            data = self._get_price_yfinance(bool_data=True)
            self._writhing_data(data, name)
            if self.progress:
                print(f'Market.get_price writhing_data file="{name}"')
        else:
            data = self._reading_data(name)
            data = self._adjust_values(data)
            if self.progress:
                print(f'Market.get_price reading_data file="{name}"')
        return data