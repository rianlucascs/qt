
from

class Acess:

    def __init__(self, ticker, start, end, column, k, name_model, config_model):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.column = column
        self.k = k
        self.name_model = name_model
        self.config_model = config_model

        name = ticker.split('.')[0]
        self.name_config_model = ' '.join(list(map(str, config_model.values())))

    def get_path(self):
        path = f'{}'
        pass
 
class GetData(Acess):

    @property
    def reading_txt(self):
        print(Acess.get_path(self)) 
        # OR
        super().get_path()

data = GetData(
    ticker="AAPL", 
    start="2024-01-01", 
    end="2024-06-01", 
    column="Close", 
    k=10, 
    name_model="model1", 
    config_model="config1"
    ).reading_txt

