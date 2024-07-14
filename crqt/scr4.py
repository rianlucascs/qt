

"""

Objetivo:

- Analise comportamento estratégias x preço ativo
- Analise do risco e alocação de recursos

"""
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
        # Alocação risco
        list_lot = range(1, 5000)
        list_result = []
        projected = 2
        max_loss = 100 
        min_return_based_on_risk = 20
        capital_available_for_allocation = 18000 / 2
        number_of_actove_strategies = 3
        capital_allocated_to_each_strategy = capital_available_for_allocation / number_of_actove_strategies
        drawdrawn = data['serie_retorno'][data['serie_retorno'] < 0].min()
        Projected_Risk = abs(drawdrawn) * projected
        last_price = download(ticker, period='1y', progress=False)[['Adj Close']].values[-1][0]
        
        print(f'# RISK')
        print(f'ticker: {ticker}')
        print(f'min_return_based_on_risk: {min_return_based_on_risk}')
        print(f'capital_available_for_allocation: {capital_available_for_allocation}')
        print(f'number_of_actove_strategies: {number_of_actove_strategies}')
        print(f'capital_allocated_to_each_strategy: {capital_allocated_to_each_strategy}')
        print(f'drawdrawn: {drawdrawn}')
        print(f'Projected_Risk: {Projected_Risk}')
        print(f'last_price: {last_price}')

        average_return_based_on_risk = lambda lot: lot * data['serie_retorno'].mean()

        for lot in list_lot:
            if lot <= 100 or str(lot).endswith('00') or str(lot).endswith('000'):
                calc = lot * last_price * (Projected_Risk / 100)
                if calc <= max_loss:
                    cost = last_price * lot 
                    if cost <= capital_allocated_to_each_strategy:
                        list_result.append([lot, calc, cost, average_return_based_on_risk(lot)])
                else:
                    if calc <= max_loss * 3:
                        if average_return_based_on_risk(lot) < min_return_based_on_risk:
                            cost = last_price * lot
                            if cost <= capital_allocated_to_each_strategy:
                                list_result.append([lot, calc, cost, average_return_based_on_risk(lot)])
                    else:
                        if average_return_based_on_risk(lot) < min_return_based_on_risk:
                            cost = last_price * lot
                            if cost <= capital_allocated_to_each_strategy:
                                list_result.append([lot, calc, cost, average_return_based_on_risk(lot)])
                                
        print(f'\nLot: {list_result[-1][0]}')
        print(f'Max risk expected: {list_result[-1][1]:.2f}')
        print(f'Cost: {list_result[-1][2]:.2f}')
        print(f'Average return based on risk: {list_result[-1][3]:.2f}')
        print()


class Analysis(Template):

    def main(self):
        data = Template(self.ticker, self.start, self.end, self.features).result_model_after_creation

        dataA = Tests.B(data[0], self.ticker)



if __name__ == '__main__':
    ticker = 'arzz3.sa'
    start = '2013-06-15'
    end='2023-06-15'
    features = [52, 82]
    Analysis(ticker, start, end, features).main()