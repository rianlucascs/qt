from utils import PATH
from strats.template import Template
from numpy import float64
from utils.graphics import Graphic
from pandas import set_option

class Infos(Template):
    
    def graphic(self, dataB):
        pb = dataB[0].reset_index()
        Graphic(pb, 'Date', ['adj_close', 'retorno_modelo']).scale()

    def metrics(self, dataA, dataB):

        ma = dataA[1]
        mb = dataB[1]

        labels = ['Acurácia Treino', 'Acurácia Test', 'Percentual Dias Positivo Total', 'Percentual Dias Positivo Teste', 
                  'Dados Perdidos', 'Quantidade de sinais teste (venda, compra)', 'Quantidade de sinais treino (venda, compra)',
                  'Quantidade de sinais total (venda, compra)', 'Diferência (Acurácia treino - Acurácia teste)',
                  'Média da série do retorno do modelo', 'Desvio padrão do retorno do modelo']
    
        print('\n# MODEL RESULT DURING CREATION\n')
        for i, item in enumerate(ma):
            if type(item) is float or type(item) is float64:
                item = f'{item:.3f}'
            print(f'{labels[i]}:'.ljust(50), item)

        labels = ['Quantidade de sinais total (venda, compra)', 'Média da série do retorno do modelo', 
                  'Desvio padrão do retorno do modelo']
        print(f'\n# RESULT MODEL AFTER CREATION\n')
        for i, item in enumerate(mb):
            if type(item) is float or type(item) is float64:
                item = f'{item:.3f}'
            print(f'{labels[i]}:'.ljust(50), item)

        pb = dataB[0].reset_index()
        Graphic(pb, 'Date', ['adj_close', 'retorno_modelo']).scale()
    
    def returns(self, dataB, lot):
        pb = dataB[0].reset_index()
        pb['year'] = pb['Date'].dt.year
        pb['month'] = pb['Date'].dt.month
        sum_per_month = pb.groupby(['year', 'month'])['serie_retorno'].sum()
        print(round(sum_per_month * lot, 2))
        sum_per_year = pb.groupby('year')['serie_retorno'].sum()
        print(round(sum_per_year * lot, 2))

    def features_serie(self, dataB):
        features = ['f'+str(f) for f in self.features] + ['previsto', 'alvo', 'alvo_bin']
        print(dataB[0][features].tail(20))


    def main(self, lot):
        data = Template(self.ticker, self.start, self.end, self.features)
        dataA = data.model_result_during_creation
        dataB = data.result_model_after_creation
        self.metrics(dataA, dataB)
        self.returns(dataB, lot)
        self.features_serie(dataB)

if __name__ == '__main__':
    """

    Objetivo:

    - Visualização resultados

    """
    
    set_option('display.max_rows', None)

    ticker = 'hype3.sa'
    start = '2013-06-15'
    end = '2023-06-15'
    features = [30, 64, 2]

    lot = 53
    
    infos = Infos(ticker, start, end, features)
    infos.main(lot)