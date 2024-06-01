from data.data import Market

from utils import PATH

from strats.template import Template

# data = Market('goau4.sa', '2012-06-15', '2022-06-15').get_price
# print(data)
Template('goau4.sa', '2012-06-15', '2022-06-15').main()