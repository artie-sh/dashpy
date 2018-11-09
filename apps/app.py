# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from database_writer import CsvReader
from dash.dependencies import Input, Output
from data_processor import DataProcessor

class Aplication:

    app = None
    db_reader = None
    dp = None

    table_name = 'xrp'
    styles = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    colors = { 'background': '#111111', 'text': '#7FDBFF' }

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=self.styles)
        self.db_reader = CsvReader()
        self.dp = DataProcessor(self.db_reader.read_db(self.db_reader.connect_db(self.db_reader.db_path), self.table_name))
        self.draw_layout('open')

        @self.app.callback(
            Output(component_id='graph', component_property='figure'),
            [Input(component_id='options', component_property='value')]
        )
        def draw_graph(input_value):
            data_rows = self.dp.get_data_rows(input_value)
            data_rows.name = input_value
            mav = self.dp.calc_moving_average(150)
            mav.name = 'mav'
            return {'data': [data_rows, mav]}

        self.app.run_server(debug = True)


    def draw_layout(self, type):
        self.app.layout = html.Div(children=[
            html.H4(children='XRP/USD', style={'text-align':'center'}),

            html.Div(children=[

                html.Div(children=
                    dcc.Graph(id='graph'),
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

            ], style={'text-align':'center', 'border': '1px solid black', 'display': 'table', 'width':'100%'}),
            html.Div
        ])


if __name__ == '__main__':
    app = Aplication()