
from utils import PATH
from strats.template import Template
from pandas import concat
import matplotlib.pyplot as plt
from pandas import set_option

class AnalyzesTheReturnOfAllStrategies:
    
    def main(**kwargs):
        
        data1 = Template(
            kwargs.get('ticker1'), 
            kwargs.get('start1'), 
            kwargs.get('end1'), 
            kwargs.get('features1')
            ).result_model_after_creation
        serie1 = data1[0]['serie_retorno'] * kwargs.get('lot1')
        
        data2 = Template(
            kwargs.get('ticker2'), 
            kwargs.get('start2'), 
            kwargs.get('end2'), 
            kwargs.get('features2')
            ).result_model_after_creation
        serie2 = data2[0]['serie_retorno'] * kwargs.get('lot2')
        
        # data3 = Template(
        #     kwargs.get('ticker3'), 
        #     kwargs.get('start3'), 
        #     kwargs.get('end3'), 
        #     kwargs.get('features3')
        #     ).result_model_after_creation
        # serie3 = data3[0]['serie_retorno'] * kwargs.get('lot1')
        
        # data = concat([serie1, serie2, serie3], axis=1)

        data = concat([serie1, serie2], axis=1)

        data = data.fillna(0)
        # data.columns = ['1', '2', '3']
        data.columns = ['1', '2']
        # data['return'] = data['1'] + data['2'] + data['3']
        data['return'] = data['1'] + data['2']
        data = data.reset_index()

        data['year'] = data['Date'].dt.year
        data['month'] = data['Date'].dt.month
        sum_per_month = data.groupby(['year', 'month'])['return'].sum()
        print(round(sum_per_month, 2))
        sum_per_year = data.groupby('year')['return'].sum()
        print(round(sum_per_year, 2))

        plt.plot(data['return'].cumsum())
        plt.show()
    
        
if __name__ == '__main__':

    """
    
    Objetivo:

    - Analisa o retorno de todas as estratégias
    
    """
    
    set_option('display.max_rows', None)
    
    AnalyzesTheReturnOfAllStrategies.main(
        ticker1 = 'azul4.sa',
        start1 = '2017-04-11',
        end1 = '2023-06-15',
        features1 = [134, 138, 58],
        lot1 = 100,

        ticker2 = 'hype3.sa',
        start2 = '2013-06-15',
        end2 = '2023-06-15',
        features2 = [30, 64, 2],
        lot2 = 100,

        # ticker3 = 'arzz3.sa',
        # start3 = '2013-06-15',
        # end3 = '2023-06-15',
        # features3 = [12, 18, 96],
        # lot3 = 53
    )