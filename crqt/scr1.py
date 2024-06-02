from data.data import Market

from utils import PATH

from strats.template import Template

# data = Market('goau4.sa', '2012-06-15', '2022-06-15').get_price
# print(data)


data = Template('goau4.sa', '2012-05-15', '2022-05-15', [40, 21, 24, 28, 104, 101]).result_model_after_creation
print(data[1])
# print(data[1])
# data = data[0]

# data = data.reset_index()

# data['year'] = data['Date'].dt.year
# data['month'] = data['Date'].dt.month
# print(data)
# soma_por_ano_mes = data.groupby(['year', 'month'])['serie_retorno'].sum()

# print(soma_por_ano_mes * 100)
# from pandas import to_datetime

# date = to_datetime('2015-02-02')
# # print(date)
# print(data[0].iloc[1])