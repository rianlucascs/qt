from utils.data import Market

# Market('goau4.sa', '2012-05-15', '2022-05-15', yf=True).get_price
Market('goau4.sa', period='1y', progress=False).get_price