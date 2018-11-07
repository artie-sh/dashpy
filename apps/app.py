# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dateparser
from database_writer import CsvReader

import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

#df = pd.read_csv('./xrp.csv')
reader = CsvReader()
df = reader.read_db(reader.connect_db(reader.db_path))

columns = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

def getDataRows(df, column_name):
    coords = dict()
    for row in df:
        coords[row[0]] = row[columns[column_name]]
    return coords

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_graph(dataframe):
    pass

coords_open = getDataRows(df, 'open')
coords_high = getDataRows(df, 'high')
coords_low = getDataRows(df, 'low')
coords_close = getDataRows(df, 'close')

app.layout = html.Div(children=[
    html.H4(children='XRP/USD'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': sorted(coords_open.keys()), 'y': [coords_open[key] for key in sorted(coords_open.keys())], 'type': 'linear', 'name': 'Open'},
                {'x': sorted(coords_high.keys()), 'y': [coords_high[key] for key in sorted(coords_high.keys())], 'type': 'linear', 'name': 'High'},
                {'x': sorted(coords_low.keys()), 'y': [coords_low[key] for key in sorted(coords_low.keys())], 'type': 'linear', 'name': 'Low'},
                {'x': sorted(coords_close.keys()), 'y': [coords_close[key] for key in sorted(coords_close.keys())], 'type': 'linear', 'name': 'Close'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)