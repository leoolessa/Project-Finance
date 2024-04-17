import os 
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app 

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd 





#--Layout--#
layout =  dbc.Col([
    html.H1('MyBudget', className='text-primary'),
    html.P('By Lessa', className='text-info'),
    html.Hr(),
    
    #--Perfil--#
    dbc.Button(id='avatar_button',
               children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                         ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
    
    #--New Section--#
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='open-new-income',
                       children=['+ Income'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='open-new-expense',
                       children=['- Expenses'])
        ], width=6)
    ]),
    
    #--Nav Section--#
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink('Dashboard', href='/dashboards', active='exact'),
            dbc.NavLink('Statements', href='/statements', active='exact'),
        ], vertical=True, pills=True, id='nav_buttons', style={'margin-button': '50px'}),
    
], id='complete_sidebar')
