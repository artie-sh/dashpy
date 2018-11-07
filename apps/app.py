# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from database_writer import CsvReader
from dash.dependencies import Input, Output


class Aplication:

    app = None
    db_reader = None
    df = None

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    colors = { 'background': '#111111', 'text': '#7FDBFF' }
    columns = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.db_reader = CsvReader()
        self.df = self.db_reader.read_db(self.db_reader.connect_db(self.db_reader.db_path))
        self.buildGraph()

        @self.app.callback(
            Output(component_id='my-div', component_property='children'),
            [Input(component_id='my-id', component_property='value')]
        )
        def update_output_div(input_value):
            return 'You\'ve entered "{}"'.format(input_value)

        self.app.run_server(debug = True)

    def getDataRows(self, df, column_name):
        coords = dict()
        for row in df:
            coords[row[0]] = row[self.columns[column_name]]
        return coords

    def buildGraph(self):
        coords_open = self.getDataRows(self.df, 'open')
        coords_high = self.getDataRows(self.df, 'high')
        coords_low = self.getDataRows(self.df, 'low')
        coords_close = self.getDataRows(self.df, 'close')

        self.app.layout = html.Div(children=[
            html.H4(children='XRP/USD', style={'text-align':'center'}),
            html.Div(children=[
                html.Div(children=
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [
                                {'x': sorted(coords_open.keys()),
                                 'y': [coords_open[key] for key in sorted(coords_open.keys())], 'type': 'linear',
                                 'name': 'Open'},
                                {'x': sorted(coords_high.keys()),
                                 'y': [coords_high[key] for key in sorted(coords_high.keys())], 'type': 'linear',
                                 'name': 'High'},
                                {'x': sorted(coords_low.keys()),
                                 'y': [coords_low[key] for key in sorted(coords_low.keys())], 'type': 'linear',
                                 'name': 'Low'},
                                {'x': sorted(coords_close.keys()),
                                 'y': [coords_close[key] for key in sorted(coords_close.keys())], 'type': 'linear',
                                 'name': 'Close'},
                            ],
                            'layout': {'title': 'Dash Data Visualization'}
                        }
                    ),
                    style={'display': 'table-cell', 'width': '95%', 'border': '1px solid blue'}
                ),
                html.Div(children=
                    dcc.Checklist(
                        id='options',
                        options=[
                            {'label': 'Open', 'value': 'open'},
                            {'label': 'High', 'value': 'high'},
                            {'label': 'Low', 'value': 'low'},
                            {'label': 'Close', 'value': 'close'}
                        ],
                        values=[]
                    ),
                    style={'text-align': 'left', 'display': 'table-cell', 'width':'5%', 'border': '1px solid green', 'vertical-align':'middle'}
                )
            ]
            , style={'text-align':'center', 'border': '1px solid black', 'display': 'table', 'width':'100%'}),
            dcc.Input(id='my-id', value='initial value', type='text'),
            html.Div(id='my-div', style={'border': '1px solid green'})
        ])


if __name__ == '__main__':
    app = Aplication()