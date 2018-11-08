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

    table_name = 'xrp'
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    colors = { 'background': '#111111', 'text': '#7FDBFF' }
    columns_mapping = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.db_reader = CsvReader()
        self.df = self.db_reader.read_db(self.db_reader.connect_db(self.db_reader.db_path), self.table_name)
        self.buildGraph('open')

        @self.app.callback(
            Output(component_id='graph', component_property='figure'),
            [Input(component_id='options', component_property='value')]
        )
        def redraw_graph(input_value):
            return {'data': [self.getDataRows(self.df, input_value)]}

        self.app.run_server(debug = True)

    def getDataRows(self, df, column_name):
        datax = []
        datay = []
        for line in df:
            datax.append(line[0])
            datay.append(line[self.columns_mapping[column_name]])
        return go.Scatter(x=datax, y=datay, mode='lines')


    def buildGraph(self, type):
        self.app.layout = html.Div(children=[
            html.H4(children='XRP/USD', style={'text-align':'center'}),
            html.Div(children=[
                html.Div(children=
                    dcc.Graph(
                        id='graph',
                        figure={'data': [self.getDataRows(self.df, type)]}
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
            , style={'text-align':'center', 'border': '1px solid black', 'display': 'table', 'width':'100%'})
        ])


if __name__ == '__main__':
    app = Aplication()