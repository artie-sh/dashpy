# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv('./xrp.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

app.layout = html.Div(children=[
    html.H4(children='artie test table'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)