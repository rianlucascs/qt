
from utils import PATH
from strats.template import Template
from utils.graphics import Graphic
from yfinance import download

class Conditions:

    @staticmethod
    def C1(data):
        # Quantidade de previsões: compra ou venda relacionado a quantidade de vendas ou compras
        # ? Se acima da média então queremos uma maior quantidade de compras.
        for date, adj_close, mm, serie_retorno, previsto in data[['Date', 'adj_close', 'mm', 'serie_retorno', 'previsto']].values:
            if adj_close > mm:
                match previsto:
                    case 0:
                        pass
                    case 1:
                        pass

            elif adj_close < mm:
                match previsto:
                    case 0:
                        pass
                    case 1:
                        pass

class Tests:

    @staticmethod
    def A(data):
        # 
        data = data.reset_index()
        data['mm'] = data.adj_close.rolling(20).mean().dropna()
        Graphic(data, 'Date', ['adj_close', 'retorno_modelo', 'mm']).scale()
        conditions = Conditions.C1(data)

    def B(data, ticker):
        pass


class Analysis(Template):

    def main(self):
        data = Template(self.ticker, self.start, self.end, self.features).result_model_after_creation

        dataA = Tests.A(data[0])

if __name__ == '__main__':


    """

    Objetivo:

    - Analise comportamento estratégias x preço ativo

    """
    ticker = 'azul4.sa'
    start = '2017-04-11'
    end = '2023-06-15'
    features = [134, 138, 58]
    
    Analysis(ticker, start, end, features).main()


"""
    ticker = 'hype3.sa'
    start = '2013-06-15'
    end = '2023-06-15'
    features = [30, 64, 2]

    ticker = 'azul4.sa'
    start = '2017-04-11'
    end = '2023-06-15'
    features = [134, 138, 58]

"""