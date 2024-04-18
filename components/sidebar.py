import os
import dash
import json
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime, date

import pdb
from dash_bootstrap_templates import ThemeChangerAIO

# ========= DataFrames ========= #
import numpy as np
import pandas as pd
from globals import *


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
                       children=['+ Income']),
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='open-new-expense',
                       children=['- Expenses']),
        ], width=6)
    ]),
        
    #--Income Modal
    html.Div([
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Add Income')),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Description: '),
                        dbc.Input(placeholder='E.g: Salary, Extra Earnings, Investments...', id='txt-income'),
                    ], width=6),
                    dbc.Col([
                        dbc.Label('Value: '),
                        dbc.Input(placeholder=' € 100,00', id='value_income', value='')
                    ], width=6),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Date: '),
                        dcc.DatePickerSingle(id='date-income', 
                            min_date_allowed=date(2020,1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            style={'width': '100%'}
                            ),
                    ], width=4),
                    
                    dbc.Col([
                        dbc.Label('Extra Options'),
                        dbc.Checklist(
                            options=[{"label": "Was Received", "value": 1},
                                    {"label": "Regular Expense", "value": 2}],
                            value=[1],
                            id='switches-input-income',
                            switch=True
                        ),
                    ], width=4),
                    
                    dbc.Col([
                        html.Label('Income Category'),
                        dbc.Select(id='select_income', options=[{'label': i, 'value': i} for i in cat_income], value=cat_income)
                    ], width=4),
                ],style={"margin-top": "25px"}), 
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend('Add Category', style={'color': 'green'}),
                                    dbc.Input(type='text', placeholder='New Category', id='input-category-income', value=''),
                                    html.Br(),
                                    dbc.Button('Add', className='tbn btn-success', id='add-category-income', style={'margin-top': '20px'}),
                                    html.Br(),
                                    html.Div(id='category-div-add-income', style={}),
                                ], width=6),
                                dbc.Col([
                                    html.Label('Remove categories', style={'color':'red'}),
                                    dbc.Checklist(
                                        options=[],
                                        value=[],
                                        id='checklist-selected-style-income',
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={'backgroundColor': 'blue', 'borderColor':'orange'}
                                    ),
                                    dbc.Button('Remove', color='warning', id='remove-category-income', style={'margin-top': '20px'})
                                ], width=6)
                            ]),
                        ], title='Add/Remove Categories'),
                    ], flush=True, start_collapsed=True, id='accordion-income'),
                    
                        html.Div(id='id_test_income', style={'padding-top': '20px'}),
                        
                        dbc.ModalFooter([
                            dbc.Button('Add Income', id='save_income', color='success'),
                            dbc.Popover(dbc.PopoverBody('Income Saved'), target='save_income', placement='left', trigger='click'),
                        ])
                ], style={'margin-top': '25px'}),
            ])
        ], 
        style={"background-color": "rgba(17, 140, 79, 0.05)"},
        id='modal-new-income',
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True),
    ]),
    
    
    #--Expenses Modal--#
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Add Expense')),
        dbc.ModalBody([
            dbc.Row([
                    dbc.Col([
                        dbc.Label('Description: '),
                        dbc.Input(placeholder='E.g: Rent, Bills, Supermarket...', id='txt-expense'),
                    ], width=6),
                    dbc.Col([
                        dbc.Label('Value: '),
                        dbc.Input(placeholder=' € 100,00', id='value_expense', value='')
                    ], width=6),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Date: '),
                        dcc.DatePickerSingle(id='date-expense', 
                            min_date_allowed=date(2020,1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            style={'width': '100%'}
                            ),
                    ], width=4),
                    
                    dbc.Col([
                        dbc.Label('Extra Options'),
                        dbc.Checklist(
                            options=[{"label": "Was Received", "value": 1},
                                    {"label": "Regular Expense", "value": 2}],
                            value=[1],
                            id='switches-input-expense',
                            switch=True
                        ),
                    ], width=4),
                    
                    dbc.Col([
                        html.Label('Expense Category'),
                        dbc.Select(
                            id='select_expense', options=[{'label': i, 'value': i} for i in cat_expense], value=cat_expense)
                    ], width=4),
                ],style={"margin-top": "25px"}), 
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend('Add Category', style={'color': 'green'}),
                                    dbc.Input(type='text', placeholder='New Category', id='input-category-expense', value=''),
                                    html.Br(),
                                    dbc.Button('Add', className='tbn btn-success', id='add-category-expense', style={'margin-top': '20px'}),
                                    html.Br(),
                                    html.Div(id='category-div-add-expense', style={}),
                                ], width=6),
                                dbc.Col([
                                    html.Label('Remove categories', style={'color':'red'}),
                                    dbc.Checklist(
                                        options=[],
                                        value=[],
                                        id='checklist-selected-style-expense',
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={'backgroundColor': 'blue', 'borderColor':'orange'}
                                    ),
                                    dbc.Button('Remove', color='warning', id='remove-category-expense', style={'margin-top': '20px'})
                                ], width=6)
                            ]),
                        ], title='Add/Remove Categories'),
                    ], flush=True, start_collapsed=True, id='accordion-expense'),
                    
                        dbc.ModalFooter([
                            dbc.Button('Add Expense', id='save_expense', color='success'),
                            dbc.Popover(dbc.PopoverBody('Expense Saved'), target='save_expense', placement='left', trigger='click'),
                        ])
                ], style={'margin-top': '25px'}),
            ])
        
    ], 
    style={"background-color": "rgba(17, 140, 79, 0.05)"},
    id='modal-new-expenses',
    size="lg",
    is_open=False,
    centered=True,
    backdrop=True),
        
        
    #--Nav Section--#
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink('Dashboard', href='/dashboards', active='exact'),
            dbc.NavLink('Statements', href='/statements', active='exact'),
        ], vertical=True, pills=True, id='nav_buttons', style={'margin-button': '50px'}),
    
], id='complete_sidebar')




#--Callbacks--#
#pop-Up statement 



#Pop-Up Expenses
@app.callback(
    Output('modal-new-expenses', 'is_open'),
    Input('open-new-expense', 'n_clicks'),
    State('modal-new-expenses', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    
    
#Pop-Up Income
@app.callback(
    Output('modal-new-income', 'is_open'),
    Input('open-new-income', 'n_clicks'),
    State('modal-new-income', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
        
        
# Send income form
@app.callback(
    Output('store-income', 'data'),

    Input("salve_income", "n_clicks"),

    [
        State("txt-income", "value"),
        State("value_income", "value"),
        State("date-income", "date"),
        State("switches-input-income", "value"),
        State("select_income", "value"),
        State('store-income', 'data')
    ]
)      

  
def salve_form_income(n, description, value, date, switches, category, dict_income):
    df_incomes = pd.DataFrame(dict_income)

    if n and not(value == "" or value== None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        completed = 1 if 1 in switches else 0
        regular = 0 if 2 in switches else 0

        df_incomes.loc[df_incomes.shape[0]] = [value, completed, regular, date, category, description]
        df_incomes.to_csv("data/df_incomes.csv")

    data_return = df_incomes.to_dict()
    return data_return


# Send Expenses form
@app.callback(
    Output('store-expense', 'data'),

    Input("salve_expense", "n_clicks"),

    [
        State("value_expense", "value"),
        State("switches-input-expense", "value"),
        State("select_expense", "value"),
        State("date-expense", "date"),
        State("txt-expense", "value"),
        State('store-expense', 'data')
    ]
)


def salve_form_expense(n, description, value, date, switches, category, dict_income):
    df_expenses = pd.DataFrame(dict_income)

    if n and not(value == "" or value== None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        completed = 1 if 1 in switches else 0
        regular = 0 if 2 in switches else 0

        df_expenses.loc[df_expenses.shape[0]] = [value, completed, regular, date, category, description]
        df_expenses.to_csv("data/df_incomes.csv")

    data_return = df_expenses.to_dict()
    return data_return