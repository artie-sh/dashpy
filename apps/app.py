# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dateparser
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

df = pd.read_csv('./xrp.csv')

# def avg(values):
#     return sum(values)/len(values)

def getDataRows(df):
    coords = dict()
    for row in df.iterrows():
        r = list(row[1])
        coords[dateparser.parse(r[0])] = r[2]
    return coords

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_graph(dataframe):
    pass

coords = getDataRows(df)

app.layout = html.Div(children=[
    html.H4(children='artie test table'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': sorted(coords.keys()), 'y': [coords[key] for key in sorted(coords.keys())], 'type': 'linear', 'name': 'XRP/USD'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)