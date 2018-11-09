import plotly.graph_objs as go
from database_writer import CsvReader

class DataProcessor():

    data = None
    columns_mapping = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

    def __init__(self, data):
        self.data = data

    def get_data_rows(self, column_name):
        datax = []
        datay = []
        for line in self.data:
            datax.append(line[0])
            datay.append(line[self.columns_mapping[column_name]])
        return go.Scatter(x=datax, y=datay, mode='lines')

    def calc_moving_average(self, periods):
        datax = [line[0] for line in self.data[:periods-1]]
        datay = [None] * (periods - 1)
        for i in range(periods-1, len(self.data)):
            datax.append(self.data[i][self.columns_mapping['date']])
            datay.append(self.avg([line[self.columns_mapping['open']] for line in self.data[i-(periods-1):i+1]]))
        return go.Scatter(x=datax, y=datay, mode='lines')


    def avg(self, values):
        sum = 0
        for value in values:
            sum += value
        return sum/len(values)



# db = CsvReader()
# dp = DataProcessor(db.read_db(db.connect_db(db.db_path), 'xrp'))
# dp.calc_moving_average(5)