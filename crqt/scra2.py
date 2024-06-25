
from yfinance import download
from tools.create_list_tickers import TickersMt5


class ConditionsAndCalculations:

    def __init__(self, data):
        self.data = data

    def _bool_day_high_or_low(self, data):
        

        


class VolatilityAnalysis:

    def __init__(self):
        self.tickers = TickersMt5().get()
        
    def data(self, ticker):
        return download(ticker, period='5y', progress=False)

    def loop(self):
        for ticker in self.tickers:
            data = self.data(ticker)
            cond_calc = ConditionsAndCalculations(data)

            print(data)
            break

if __name__ == '__main__':
    VolatilityAnalysis().loop()