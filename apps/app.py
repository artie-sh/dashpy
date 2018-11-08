# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from database_writer import CsvReader
from dash.dependencies import Input, Output
import plotly.graph_objs as go

class Aplication:

    app = None
    db_reader = None
    df = None

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    colors = { 'background': '#111111', 'text': '#7FDBFF' }
    columns_mapping = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.db_reader = CsvReader()
        self.df = self.db_reader.read_db(self.db_reader.connect_db(self.db_reader.db_path))
        self.buildGraph('open')

        @self.app.callback(
            Output(component_id='graph', component_property='figure'),
            [Input(component_id='options', component_property='value')]
        )
        def redraw_graph(input_value):
            coords = self.getDataRows(self.df, input_value)
            datax = []
            datay = []
            data = []
            for key in sorted(coords.keys()):
                datax.append(key)
                datay.append(coords[key])
            data.append(go.Scatter(x=datax, y=datay, mode='lines'))
            return {
                    'data': data,
                    'layout': {'title': 'Dash Data Visualization'}
                    }

        self.app.run_server(debug = True)

    def getDataRows(self, df, column_name):
        coords = dict()
        for row in df:
            coords[row[0]] = row[self.columns_mapping[column_name]]
        return coords

    def buildGraph(self, type):
        coords = self.getDataRows(self.df, type)

        self.app.layout = html.Div(children=[
            html.H4(children='XRP/USD', style={'text-align':'center'}),
            html.Div(children=[
                html.Div(children=
                    dcc.Graph(
                        id='graph',
                        figure={
                            'data': {'x': coords.keys(), 'y': [coords[key] for key in coords.keys()], 'type': 'linear', 'name': type},
                            'layout': {'title': 'Dash Data Visualization'},
                        }
                    ),
                    style={'display': 'table-cell', 'width': '95%', 'border': '1px solid blue'}
                ),
                html.Div(children=
                    dcc.RadioItems(
                        id='options',
                        options=[
                            {'label': 'open', 'value': 'open'},
                            {'label': 'high', 'value': 'high'},
                            {'label': 'low', 'value': 'low'},
                            {'label': 'close', 'value': 'close'}
                        ],
                        value='open'
                    ),
                    style={'text-align': 'left', 'display': 'table-cell', 'width':'5%', 'border': '1px solid green', 'vertical-align':'middle'}
                )
            ]
            , style={'text-align':'center', 'border': '1px solid black', 'display': 'table', 'width':'100%'}),
            html.Div(id='my-div', style={'border': '1px solid green'})
        ])


if __name__ == '__main__':
    app = Aplication()