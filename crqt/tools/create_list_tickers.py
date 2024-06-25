


import MetaTrader5 as mt5
from sys import path
from os import remove
from os.path import exists

class TickersMt5:

    def __init__(self):
        self._path = path[0].replace('\\tools', '') + '\\data\\tickers\\tickers_mt5.txt'

    @staticmethod
    def get_mt5():
        symbols = mt5.symbols_get()
        lista_sybols = []
        for s in symbols:
            key1 = s.path.split('\\')
            if key1[0] == 'BOVESPA' and key1[1] == 'A VISTA':
                key2 = s.description.split(' ')
                if 'ON' in key2 or 'PN' in key2:
                    if not s.name[-1].isalpha():
                        lista_sybols.append(s.name) 
        return lista_sybols
    
    def get(self):
        with open(self._path, 'r', encoding='utf-8') as file:
            file = file.read()[1:-1].replace("'", '').split(', ')
            file = [item+'.SA' for item in file]
            return file
    
    def main(self):
        if exists(self._path):
            remove(self._path)
        with open(self._path, 'a', encoding='utf-8') as file:
            file.write(self.get_mt5().__str__())
        return None
    
if __name__ == '__main__':
    mt5.initialize()
    tickers_mt5 = TickersMt5()
    tickers_mt5.main()


