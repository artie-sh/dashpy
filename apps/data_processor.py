import plotly.graph_objs as go


class DataProcessor():

    data = None
    columns_mapping = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

    def __init__(self, data):
        self.data = data

    def getDataRows(self, column_name):
        datax = []
        datay = []
        for line in self.data:
            datax.append(line[0])
            datay.append(line[self.columns_mapping[column_name]])
        return go.Scatter(x=datax, y=datay, mode='lines')
