from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import dashboards, sidebar, statements
from globals import *




#--Layout--#
content = html.Div(id='page-content')


app.layout = dbc.Container(children=[
    dcc.Store(id='store-expenses', data=df_expenses.to_dict()),
    dcc.Store(id='store-incomes', data=df_incomes.to_dict()),
    dcc.Store(id='store-cat-expenses', data=df_cat_expense.to_dict()),
    dcc.Store(id='store-cat-incomes', data=df_cat_income.to_dict()),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        dbc.Col([
            content
        ], md=10)
    ])    
], fluid=True,)


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])


def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    if pathname == '/statements':
        return statements.layout


if __name__ == '__main__':
    app.run_server(debug=True)