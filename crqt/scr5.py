
from utils import PATH
from strats.template import Template
from crqt.scr2 import inventory_features

class FilterCombinationStrategy:

    def __init__(self, dataA, dataB):
        # NEW
        self.PA = dataA[0] # perfomance, model_result_during_creation, new
        self.MA = dataA[1] # metric, model_result_during_creation, new

        self.PB = dataB[0] # performance, result_model_after_creation, new
        self.MB = dataB[1] # metric, result_model_after_creation, new

    def _number_of_signals(self, data):
        try:
            x = int(((data[0] + data[1]) * (1/3)))
        except:
            return False
        if (data[0] >= x) and (data[1] >= x):
            return True
        return False

    def _overfitting(self, data):
        if data <= 3:
            return True
        return False
    
    def _percentage_positive_days(self, data):
        if data > 0.50:
            return True
        return False

    def apply(self):
        
        if (
            self._number_of_signals(self.MB[0]) and # Quantidade de sinais pós treino e teste
            self._number_of_signals(self.MA[5]) and # Quantidade de sinais treino
            self._number_of_signals(self.MA[6]) and # Quantidade de sinais teste
            self._number_of_signals(self.MA[7]) and # Quantidade de sinais total treino e teste
            self._overfitting(self.MA[8]) and # Overfitting
            self._percentage_positive_days(self.MA[2]) and # Porcentage dias positivos total
            self._percentage_positive_days(self.MA[3]) # Porcentage dias positivos teste
            ):
            return True

class Visualize:

    @staticmethod
    def text_metric(f, A, B):
        q = lambda x: f'{x:.2f}'
        w = lambda x: f'{x:.3f}'
        e = lambda x, y: f'{x}'.ljust(y)
        s = ' | '
        # print(f'{e(f,25)}{s}{q(A[0])}{s}{q(A[1])}{s}{w(A[2])}{s}{w(A[3])}{s}{e(A[4],5)}{s}{e(A[5],12)}{s}{e(A[6],12)}{s}{e(A[7],12)}{s}{w(A[8])}{s}{w(A[9])}{s}{e(B[0],12)}{s}{w(B[1])}')
        try:
            print(f'{e(f,20)}{s}{w(A[2])}{s}{w(A[3])}{s}{e(A[4],5)}{s}{e(A[5],12)}{s}{e(A[6],12)}{s}{e(A[7],12)}{s}{w(A[8])}{s}{e(w(A[9]), 7)}{s}{e(B[0],12)}{s}{w(B[1])}')
        except:
            print(f, A, B)

class Otimization(Template):

    def main(self, fails=False):
        print(Template(self.ticker, self.start, self.end, self.features).model_result_during_creation[1])
        print(Template(self.ticker, self.start, self.end, self.features).result_model_after_creation[1])
        for f in inventory_features():
            f = self.features + [f]

            data = Template(self.ticker, self.start, self.end, f)
            dataA = data.model_result_during_creation
            dataB = data.result_model_after_creation

            filter_combination_strategy = FilterCombinationStrategy(dataA, dataB)
            if filter_combination_strategy.apply():
                Visualize.text_metric(f, dataA[1], dataB[1])
            else:
                if fails:
                    Visualize.text_metric(f, dataA[1], dataB[1])


if __name__ == '__main__':
    
    ticker = 'arzz3.sa'
    start = '2013-06-15'
    end = '2023-06-15'
    features = [12, 18, 96]

    fails = False

    otimization = Otimization(ticker, start, end, features)
    otimization.main(fails)
    