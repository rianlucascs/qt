

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
               'FIEI3.SA', 'TEKA4.SA', 'BGIP4.SA']

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

"""
# ANALYSUS_2

# Columns

ticker
mm_vol_d
amp_mm_sombras
amp_mm_sombras_d_alta
amp_mm_sombras_d_baixa
mm_d_alta
mm_d_baixa
amostra

Amount of initial data: 322

Amount of initial data: 261
column: mm_vol_d
mean: 0.04735668589517944

Amount of initial data: 46
column: amp_mm_sombras_d_alta
mean: 4.135118361770499
number mean: 4.135118361770499

Amount of initial data: 34
column: amp_mm_sombras_d_baixa
mean: 0.36811370159652523
number mean: 0.36811370159652523



      ticker  mm_vol_d  amp_mm_sombras  amp_mm_sombras_d_alta  amp_mm_sombras_d_baixa  mm_d_alta  mm_d_baixa  amostra predominancia
0   BGIP4.SA  0.055763        0.244610               0.650293                0.108625   0.323411    0.293644     1243           Buy
1   BRKM3.SA  0.076503        0.581503               0.990000                0.278916   0.422830    0.563505     1244          Sell
2   CEEB3.SA  0.097058        0.293682               1.033250                0.367128   0.225080    0.156752     1244           Buy
3   CSRN3.SA  0.086549        0.175768               0.758980                0.191905   0.205149    0.101368     1243           Buy
4   CVCB3.SA  0.050406        0.325932               0.549775                0.164587   0.419614    0.563505     1244          Sell
5   EKTR4.SA  0.053762        0.176688               0.952816                0.140743   0.165595    0.118971     1244           Buy
6   GFSA3.SA  0.104489        0.681963               1.368007                0.251146   0.378617    0.591640     1244          Sell
7   GOLL4.SA  0.048650        0.391841               0.679481                0.172478   0.434084    0.554662     1244          Sell
8   JFEN3.SA  0.055410        0.321865               0.871747                0.155808   0.266881    0.492765     1244          Sell
9   LUXM4.SA  0.050523        0.094644               0.332404                0.188500   0.230088    0.088496     1243           Buy
10  MNPR3.SA  0.056058        0.283620               0.447357                0.144110   0.493162    0.411102     1243           Buy
11  OSXB3.SA  0.048304        0.267412               0.539226                0.111103   0.373794    0.561093     1244          Sell
12  RCSL4.SA  0.101383        0.409356               0.869479                0.192996   0.317524    0.537781     1244          Sell
13  SCAR3.SA  0.055338        0.550707               0.864694                0.248844   0.498392    0.459003     1244           Buy
14  SNSY3.SA  0.055129        0.230297               1.112476                0.192128   0.168810    0.200161     1244          Sell
15  TEKA4.SA  0.087715        0.441247               0.884420                0.265561   0.395012    0.329847     1243           Buy
16  TELB4.SA  0.109285        0.497283               1.008475                0.206653   0.368971    0.576367     1244          Sell
17  VIVR3.SA  0.075937        0.446994               1.033824                0.150979   0.323151    0.552251     1244          Sell
18  AZUL4.SA  0.068754        0.594075               0.986772                0.292861   0.433280    0.556270     1244          Sell
19  FIEI3.SA  0.068786        0.188481               1.062102                0.204692   0.156752    0.104502     1244           Buy



      ticker  maximum_amount_of_data_available  lest_price mean_volume
0   BGIP4.SA                              4094   22.080000    1.06e+03
1   BRKM3.SA                              5453   18.330000    1.29e+04 < 
2   CEEB3.SA                              6150   39.500000    5.00e+02
3   CSRN3.SA                              6149   23.030001    4.76e+02
4   CVCB3.SA                              2622    1.990000    6.69e+06
5   EKTR4.SA                              6150   39.549999    3.27e+02
6   GFSA3.SA                              5206    3.420000    4.94e+05
7   GOLL4.SA                              4982    1.120000    3.97e+06
8   JFEN3.SA                              6150    0.520000    9.99e+03
9   LUXM4.SA                              4094   13.990000    1.65e+03
10  MNPR3.SA                              6149   11.400000    8.36e+03
11  OSXB3.SA                              3642    3.930000    1.89e+04
12  RCSL4.SA                              6146    1.170000    6.65e+04
13  SCAR3.SA                              6150   23.670000    2.49e+04
14  SNSY3.SA                              4308   12.050000    4.75e+02
15  TEKA4.SA                              6149   30.900000    2.28e+03
16  TELB4.SA                              4094    8.890000    8.09e+06
17  VIVR3.SA                              4233    2.350000    1.53e+05
18  AZUL4.SA                              1797    7.540000    7.80e+06 < 
19  FIEI3.SA                              4264   10.500000    1.01e+03
"""