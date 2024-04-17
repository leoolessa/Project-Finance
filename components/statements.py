import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO


#--Layout--#
layout = dbc.Col([
    dbc.Row([
        html.Legend('Expenses Table'),
        html.Div(id='expenses-table', className='dbc')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'margin-right': '20px'})
        ], width=9),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4('Expenses'),
                    html.Legend('€ 1000', id='expense_value_card', style={'font-size': '60px'}),
                    html.H6('Total Expenses'),
                ], style={'text-align': 'center', 'padding-top': ' 30px'})    
            )
        ], width=3)
    ]),
], style={"padding": "10px"})

