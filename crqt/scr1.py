from utils import PATH

from data import Market


from strats.template import Template

ticker = 'arzz3.sa'
start = '2013-06-15'
end='2023-06-15'
feat = [52, 82]
data = Template(ticker, start, end, feat).result_model_after_creation
data_metric = Template(ticker, start, end, feat).model_result_during_creation

print(data_metric[1])

import matplotlib.pyplot as plt
data[0]['retorno'].cumsum().plot(secondary_y=True)
data[0]['retorno_modelo'].plot()
plt.show()

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