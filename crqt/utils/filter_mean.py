
class FilterMean:

    def __init__(self, data, column, above_average=False, below_average=False, multiply_mean_by=None,
                 set_number=None, progress=True):
        self.data = data
        self.column = column
        self.above_average = above_average # acima
        self.below_average = below_average # abaixo
        self.multiply_mean_by = multiply_mean_by
        self.set_number = set_number
        self.progress_ = progress

    def progress(self, message):
        if self.progress_:
            print(message)

    def Apply(self):


        if self.above_average:
            
            if self.set_number != None:
                if self.multiply_mean_by == None:
                    self.data = self.data.loc[self.data[self.column] > self.set_number]
                else:
                    self.data = self.data.loc[self.data[self.column] > self.set_number * self.multiply_mean_by]
            
            else:
                if self.multiply_mean_by == None:
                    self.progress(f'\nMean "{self.column}": {self.data[self.column].mean()}')
                    self.data = self.data.loc[self.data[self.column] > self.data[self.column].mean()]
                else:
                    self.progress(f'\nMean "{self.column}": {self.data[self.column].mean()}\nMean "{self.column}" x multiply_mean_by: {self.data[self.column].mean() * self.multiply_mean_by}')
                    self.data = self.data.loc[self.data[self.column] > self.data[self.column].mean() * self.multiply_mean_by]

        if self.below_average:

            if self.set_number != None:
                if self.multiply_mean_by == None:
                    self.data = self.data.loc[self.data[self.column] < self.set_number]
                else:
                    self.data = self.data.loc[self.data[self.column] < self.set_number * self.multiply_mean_by]
            
            else:
                if self.multiply_mean_by == None:
                    self.progress(f'\nMean "{self.column}": {self.data[self.column].mean()}')
                    self.data = self.data.loc[self.data[self.column] < self.data[self.column].mean()]
                else:
                    self.progress(f'\nMean "{self.column}": {self.data[self.column].mean()}\nMean "{self.column}" x multiply_mean_by: {self.data[self.column].mean() * self.multiply_mean_by}')
                    self.data = self.data.loc[self.data[self.column] < self.data[self.column].mean() * self.multiply_mean_by]

        return self.data
        