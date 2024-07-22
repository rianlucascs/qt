
from utils import PATH
from strats.template import Template

class Inputs:

    def __init__(self, ticker, start, end, features, projected, max_loss, min_return_based_on_risk, 
                 capital_available_for_allocation, number_of_actove_strategies):
        
        self.data = Template(ticker, start, end, features).result_model_after_creation
        self.data_df = self.data[0]

        self.ticker = ticker
        self.start = start
        self.end = end
        self.features = features
        self.projected = projected
        self.max_loss = max_loss
        self.min_return_based_on_risk = min_return_based_on_risk
        self.capital_available_for_allocation = capital_available_for_allocation / 2
        self.number_of_actove_strategies = number_of_actove_strategies
        self.capital_allocated_to_each_strategy = self.capital_available_for_allocation / number_of_actove_strategies
        self.list_lot = range(1, 5000)
        self.last_price = self.data_df[['adj_close']].values[-1][0]
        self.drawdrawn = self.data_df['serie_retorno'][self.data_df['serie_retorno'] < 0].min()
        self.Projected_Risk = abs(self.drawdrawn) * projected
        self.mean_return = self.data_df['serie_retorno'].mean()

        self.average_return_based_on_risk = lambda lot: lot * self.mean_return

        print(f'\nticker: {ticker}, start: {start}, end: {end}, features: {features}')
        print(f'projected: {projected}')
        print(f'max_loss: R$ {max_loss}')
        print(f'min_return_based_on_risk: R$ {min_return_based_on_risk}')
        print(f'capital_available_for_allocation: R$ {capital_available_for_allocation}')
        print(f'number_of_actove_strategies: {number_of_actove_strategies}')
        print(f'capital_allocated_to_each_strategy: R$ {self.capital_allocated_to_each_strategy:.2f}')
        print(f'last_price: {self.last_price:.2f}')
        print(f'drawdrawn: {self.drawdrawn:.3f}')
        print(f'Projected_Risk: {self.Projected_Risk:.3f}')
        print(f'mean_return: {self.mean_return:.3f}')
        print(f'sample: {len(self.data_df)}')


class Risk(Inputs):

    def outputs(self, list_result):
        print(f'\nLot: {list_result[-1][0]}')
        print(f'Max risk expected: R$ {list_result[-1][1]:.2f}')
        print(f'Cost: R$ {list_result[-1][2]:.2f}')
        print(f'Average return based on risk: R$ {list_result[-1][3]:.2f}')
        print()

    def A(self):
        list_result = []
        for lot in self.list_lot:
            if lot <= 100 or str(lot).endswith('00') or str(lot).endswith('000'):
                calc = lot * self.last_price * (self.Projected_Risk / 100)
                if calc <= self.max_loss:
                    cost = self.last_price * lot 
                    if cost <= self.capital_allocated_to_each_strategy:
                        list_result.append([lot, calc, cost, self.average_return_based_on_risk(lot)])
                else:
                    if calc <= self.max_loss * 3:
                        if self.average_return_based_on_risk(lot) < self.min_return_based_on_risk:
                            cost = self.last_price * lot
                            if cost <= self.capital_allocated_to_each_strategy:
                                list_result.append([lot, calc, cost, self.average_return_based_on_risk(lot)])
                    else:
                        if self.average_return_based_on_risk(lot) < self.min_return_based_on_risk:
                            cost = self.last_price * lot
                            if cost <= self.capital_allocated_to_each_strategy:
                                list_result.append([lot, calc, cost, self.average_return_based_on_risk(lot)])
        self.outputs(list_result)

    def B(self):
        list_lot = range(1, 5000)
        list_result = []
        for lot in list_lot:
            if lot <= 100 or str(lot).endswith('00') or str(lot).endswith('000'):
                calc = lot * self.last_price * (self.Projected_Risk / 100)
                cost = self.last_price * lot
                if cost <= self.capital_allocated_to_each_strategy:
                    list_result.append([lot, calc, cost, self.average_return_based_on_risk(lot)])
        self.outputs(list_result)     

if __name__ == '__main__': 

    """
    Objetivo:

    - Analise do risco e alocação de recursos

    """

    ticker = 'hype3.sa'
    start = '2013-06-15'
    end = '2023-06-15'
    features = [30, 64, 2]
    
    projected = 2
    max_loss = 200
    min_return_based_on_risk = 40
    capital_available_for_allocation = 17500
    number_of_actove_strategies = 2

    risk = Risk(ticker, start, end, features, projected, max_loss, min_return_based_on_risk, 
         capital_available_for_allocation, number_of_actove_strategies)

    risk.A()