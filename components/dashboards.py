from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import html, dcc 
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd 

from app import app 

card_icon ={
    'color':'white',
    'textAlign':'center',
    'fontSize':30,
    'margin': 'auto'
}


#--Layout--#
layout = dbc.Col([
    dbc.Row([
        
        #--Total Balance--#
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Balance'),
                    html.H5('€ 1000,00', id='p-balance-dashboard', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-university', style=card_icon),
                    color='warning',
                    style={'maxWith':75, 'height':100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        
        #--Total Income--#
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Income'),
                    html.H5('€ 1000,00', id='p-income-dashboard', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_icon),
                    color='warning',
                    style={'maxWith':75, 'height':100, 'margin-left': '-10px'}
                )
            ])
        ], width=4)
    ])
],)
