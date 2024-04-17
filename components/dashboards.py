from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import html, dcc 
import dash_bootstrap_components as dbc
from datetime import date, datetime, timedelta
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
                    html.H5('€ 2000,00', id='p-income-dashboard', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_icon),
                    color='success',
                    style={'maxWith':75, 'height':100, 'margin-left': '-10px'}
                )
            ])
        ], width=4),
        #--Total Expenses--#
         dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Expenses'),
                    html.H5('€ 1000,00', id='p-expense-dashboard', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-meh-o', style=card_icon),
                    color='danger',
                    style={'maxWith':75, 'height':100, 'margin-left': '-10px'}
                )
            ])
        ], width=4)
    ], style={'margin': '10px'}),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filter transactions', className='card-title'),
                html.Label('Incomes Categories'),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-income',
                        clearable=False,
                        style={'width': '100%'},
                        persistence= True,
                        persistence_type='session',
                        multi=True)
                    ),
                html.Label('Expenses Categories', style={'margin-top': '10px'}),
                    dcc.Dropdown(
                        id='dropdown-expense',
                        clearable=False,
                        style={'width': '100%'},
                        persistence= True,
                        persistence_type='session',
                        multi=True
                ),
                html.Label('Analysis Period', style={'margin-top': '10px'}),
                    dcc.DatePickerRange(
                        month_format='Do MMM, YY',
                        end_date_placeholder_text='Data...',
                        start_date=datetime(2022, 4, 1).date(),
                        end_date=datetime.today() + timedelta(days=31),
                        updatemode='singledate',
                        id='date-picker-config',
                        style={'z-index': '100'}
                        ),
            ], style={'height': '100%', 'padding': '20px'})
        ], width=4),
        
        dbc.Col(
            dbc.Card(dcc.Graph(id='graph1'), style={'height': '100%', 'padding': '10px'}), width=8
        )
    ], style={'margin': '10px'}),
    
    dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=3),
        ], style={"margin": "10px"})
],)
