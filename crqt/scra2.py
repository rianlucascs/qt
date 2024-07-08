

"""

# Objetivo

- Definir os melhores ativos para criar estratégias e alocar capital
- Refinar estratégias durante a criação com base nas características do ativo

# Obs

- Executar no cmd melhora a visualização do data frame

"""
from pandas import set_option
from utils.file import read
from sys import path    
from ast import literal_eval
from pandas import DataFrame
from yfinance import download
from numpy import where

__processing_data__ = 'scr3'

pass_ticker = ['MSPA4.SA', 'MTSA3.SA', 'ODER4.SA', 'SHUL3.SA', 'MAPT4.SA', 'MTSA4.SA', 'EKTR4.SA', 'CEEB3.SA',
               'FIEI3.SA', 'TEKA4.SA', 'BGIP4.SA', 'MNPR3.SA']

class VolatilityAnalysis:

    def __init__(self):
        self.all_data = self._get_serie_metric(self.data())
        set_option('display.max_columns', None)
        set_option('display.width', 1000)
        set_option('display.expand_frame_repr', False)
        set_option('display.max_rows', 10000)

    def data(self):
        data = read(f'{path[0]}\\data\\volatility_create_data\\cacls.txt').split('\n')
        list_data = []
        for row in data:
            if row != '':
                list_data.append(literal_eval(row))
        return list_data
    
    def _transform_list_into_serie(self, data, index_0, index_check=None):
        list_info = []
        for row in data:
            if not row[0] in pass_ticker:
                if index_check == None:
                    list_info.append([row[0], row[index_0]])
                else:
                    if row[index_0][0][0] == index_check:
                        list_info.append([row[0], row[index_0][0][0], row[index_0][0][1]])

                    elif row[index_0][1][0] == index_check:
                        list_info.append([row[0], row[index_0][1][0], row[index_0][1][1]])
                    
                    elif row[index_0][2][0] == index_check:
                        list_info.append([row[0], row[index_0][2][0], row[index_0][2][1]])
            
        return DataFrame(list_info)
            

    def _get_serie_metric(self, list_data, metric=None):
        
        if metric != None:
            match metric:
                case 'média volatilidade diária': # 1
                    return self._transform_list_into_serie(list_data, 1)
                
                case 'amplitude média sombras': # 2
                    return self._transform_list_into_serie(list_data, 2)
                
                case 'amplitude média sombras dias de alta': # 3 
                    return self._transform_list_into_serie(list_data, 3, 'high')

                case 'amplitude média sombras dias de baixa': # 3 
                    return self._transform_list_into_serie(list_data, 3, 'low')

                case 'média dias de alta': # 4 
                    return self._transform_list_into_serie(list_data, 4, 'high')

                case 'média dias de baixa': # 4 
                    return self._transform_list_into_serie(list_data, 4, 'low')

                case 'tamanho amostra': # 5
                    return self._transform_list_into_serie(list_data, 5)
        else:
            data = self._get_serie_metric(list_data, 'média volatilidade diária').rename(columns={0:'ticker', 1: 'mm_vol_d'})
            data['amp_mm_sombras'] = self._get_serie_metric(list_data, 'amplitude média sombras')[1].values
            data['amp_mm_sombras_d_alta'] = self._get_serie_metric(list_data, 'amplitude média sombras dias de alta')[2].values
            data['amp_mm_sombras_d_baixa'] = self._get_serie_metric(list_data, 'amplitude média sombras dias de baixa')[2].values
            data['mm_d_alta'] = self._get_serie_metric(list_data, 'média dias de alta')[2].values
            data['mm_d_baixa'] = self._get_serie_metric(list_data, 'média dias de baixa')[2].values
            data['amostra'] = self._get_serie_metric(list_data, 'tamanho amostra')[1].values
            return data

    def _get_other_ticker_information(self, data):

        list_maximum_amount_of_data_available = []
        list_last_price = []
        list_mean_volume = []
        for ticker in data['ticker']:
            price = download(ticker, period='max', progress=False)
            list_maximum_amount_of_data_available.append(len(price))
            list_last_price.append(price['Close'].values[-1])
            list_mean_volume.append('{:.2e}'.format(price['Volume'].mean()))

        data['maximum_amount_of_data_available'] = list_maximum_amount_of_data_available
        data['lest_price'] = list_last_price
        data['mean_volume'] = list_mean_volume

        data = data[['ticker', 'maximum_amount_of_data_available', 'lest_price', 'mean_volume']]

        return data

    def remove_outliers(self, data):
        data = data.loc[data['mm_d_alta'] < 0.60]
        data = data.loc[data['mm_d_baixa'] < 0.60]
        return data

    def filter(self, data, column, calc, type, multiplier_type=None, number=None, number_mean=None):

        print(f'\nAmount of initial data: {len(data)}')

        match calc:

            case 'mean':
                data[column] = abs(data[[column]])
                mean = data[column].mean()
                print(f'column: {column}')
                print(f'mean: {mean}')
                try:
                    print(f'mean * multiplier_type: {mean * multiplier_type}\n')
                except:
                    pass
                if number_mean != None: print(f'number mean: {number_mean}')
                match type:
                    case 'above': # acima
                        if number_mean != None:
                            if multiplier_type == None:
                                data = data.loc[data[column] > number_mean]
                            else:
                                data = data.loc[data[column] > number_mean * multiplier_type]
                        else:
                            if multiplier_type == None: # multiplicador
                                data = data.loc[data[column] > data[column].mean()]
                            else:
                                data = data.loc[data[column] > data[column].mean() * multiplier_type]

                    case 'down': # abaixo
                        if number_mean != None:
                            if multiplier_type == None:
                                data = data.loc[data[column] < number_mean]
                            else:
                                data = data.loc[data[column] < number_mean * multiplier_type]
                        else:
                            if multiplier_type == None: # multiplicador
                                data = data.loc[data[column] < data[column].mean()]
                            else:
                                data = data.loc[data[column] < data[column].mean() * multiplier_type]

            case 'number':
                match type:
                    case 'above':
                        data = data.loc[data[column] > number]
                    case 'down':
                        data = data.loc[data[column] < number]

        return data.reset_index(drop=True)
    
    def filter_condition(self, data, condition, test):
        
        match condition:

            case 'predominancia':

                match test:

                    case 1:
                        # Amplitude das sombras em relação a predominancia de compra ou  venda do ativo
                        # Se aplitude da sombra dos dias de baixa < média and média de dias de baixa > média de dias de alta
                        data['predominancia'] = where(data['mm_d_alta'] > data['mm_d_baixa'], 
                                                    
                                                    # Eu quero sombras menores superiores em dias de alta
                                                    where(data['amp_mm_sombras_d_alta'] < data['amp_mm_sombras_d_baixa'], 'OK Buy', 'NOT Buy'),  # 'buy'
                                                    
                                                    # E sombras menores inferiores em dias de baixa
                                                    where(data['amp_mm_sombras_d_alta'] > data['amp_mm_sombras_d_baixa'], 'OK Sell', 'NOT Sell')) # 'sell'
                        
                        # Essa condição não parece valida para dias de alta ela não ativou 'OK buy' na amostra de 300 ativos
                        # Ou seja dias de alta não implica em sobras superiores menores. Enquanto dias de baixa possuem sombras inferiores menores.

                    case 2:
                        data['predominancia'] = where(data['mm_d_alta'] > data['mm_d_baixa'], 'Buy', 'Sell')
        return data    

    
    def mmall(self, data):
        dic = {}
        for column in data.columns:
            if column != 'ticker':
                dic[column] = data[column].mean()
        return dic

    @property
    def analysis_1(self):
        
        data = self.all_data
        
        print(50*'\n')
        print('# ANALYSUS_1\n')
        print(f'# Columns\n')
        for c in list(data.columns):
            print(c)

        data = self.filter(data, 'mm_vol_d', 'mean', 'above', multiplier_type=2)
        data = self.filter(data, 'amp_mm_sombras', 'mean', 'down', multiplier_type=1)
        data = self.filter(data, 'amostra', 'number', 'above', number=1000)
        data = self.remove_outliers(data)
        
        print(2*'\n')
        print(data)
        print(2*'\n')
        print(self._get_other_ticker_information(data))

    @property
    def analysis_2(self):
        data = self.all_data
        
        print(50*'\n')
        print('# ANALYSUS_2\n')
        print(f'# Columns\n')
        for c in list(data.columns):
            print(c)
        
        # Ativos sem volume com muita vol esta prejudicando a amostra
        
        data = self.filter(data, 'amostra', 'number', 'above', number=1000)
        data = self.filter(data, 'mm_vol_d', 'mean', 'above')

        data = self.filter(data, 'amp_mm_sombras_d_alta', 'mean', 'down', 
                           number_mean=self.mmall(data)['amp_mm_sombras_d_alta'])
        
        data = self.filter(data, 'amp_mm_sombras_d_baixa', 'mean', 'down', 
                           number_mean=self.mmall(data)['amp_mm_sombras_d_baixa'])
        
        data = self.filter_condition(data, 'predominancia', test=2)
        # data = self.remove_outliers(data)
        

        print(2*'\n')
        print(data)
        print(2*'\n')
        print(self._get_other_ticker_information(data))

if __name__ == '__main__':

    VolatilityAnalysis().analysis_2