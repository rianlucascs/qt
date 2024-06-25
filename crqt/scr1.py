from utils import PATH

from data import Market


from strats.template import Template


data = Template('azul4.sa', '2017-04-11', '2023-06-15', [77, 80]).result_model_after_creation

print(data[0])

import matplotlib.pyplot as plt
plt.plot(data[0]['retorno_modelo'])
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