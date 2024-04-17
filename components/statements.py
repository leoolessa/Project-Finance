from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import html, dcc 
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd 

from app import app 


#--Layout--#
layout = dbc.Col([
    html.H5('Statements Page')
],)

