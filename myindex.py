from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


from app import *
from components import sidebar, dashboards, statements




# DataFrames and Dcc.Store

df_incomes = pd.read_csv("data/df_incomes.csv", index_col=0, parse_dates=True)
df_incomes_aux = df_incomes.to_dict()

df_expenses = pd.read_csv("data/df_expenses.csv", index_col=0, parse_dates=True)
df_expenses_aux = df_expenses.to_dict()

list_incomes = pd.read_csv('data/df_cat_incomes.csv', index_col=0)
list_incomes_aux = list_incomes.to_dict()

list_expenses = pd.read_csv('data/df_cat_expenses.csv', index_col=0)
list_expenses_aux = list_expenses.to_dict()



#--Layout--#
content = html.Div(id='page-content')


app.layout = dbc.Container(children=[
    dcc.Store(id='store-expense', data=df_expenses_aux),
    dcc.Store(id='store-income', data=df_incomes_aux),
    dcc.Store(id='stored-cat-expense', data=list_expenses_aux),
    dcc.Store(id='stored-cat-income', data=list_incomes_aux),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        
        dbc.Col([
            html.Div(id="page-content")
        ], md=10)
    ])    
], fluid=True, style={"padding": "0px"}, className="dbc")


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])


def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    if pathname == '/statements':
        return statements.layout


if __name__ == '__main__':
    app.run_server(debug=True)