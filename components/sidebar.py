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
layout =  dbc.Card([
    html.H1('Smart Finance', className='text-primary'),
    html.P('By Lessa', className='text-info'),
    html.Hr(),
    
    #--Perfil--#
    dbc.Button(id='avatar_button',
               children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                         ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
    
     dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Select Perfil")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_hom.png", className='perfil_avatar', top=True),
                                    dbc.CardBody([
                                        html.H4("Man Profile", className="card-title"),
                                        html.P(
                                            "A Card with an example of the Man profile. Text to fill the space.",
                                            className="card-text",
                                        ),
                                        dbc.Button("To access", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_fem2.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Woman Profile", className="card-title"),
                                        html.P(
                                            "A Card with an example of the Woman profile. Text to fill the space.",
                                            className="card-text",
                                        ),
                                        dbc.Button("To access", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_home.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Home Profile", className="card-title"),
                                        html.P(
                                            "A Card with an example of the Home profile. Text to fill the space.",
                                            className="card-text",
                                        ),
                                        dbc.Button("To access",  color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_plus.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Add New Profile", className="card-title"),
                                        html.P(
                                            "This project is a prototype, the button to add a new profile is temporarily disabled!",
                                            className="card-text",
                                        ),
                                        dbc.Button("Add", color="success"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                    ]),
                ],
                style={"background-color": "rgba(0, 0, 0, 0.5)"},
                id="modal-perfil",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True
                ),  
        
    
    
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
                    ], width=6)
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
                            switch=True),
                    ], width=4),
                    
                    dbc.Col([
                        html.Label('Income Category'),
                        dbc.Select(id='select_income', options=[{'label': i, 'value': i} for i in cat_income], value=[])
                    ], width=4),
                ],style={"margin-top": "25px"}), 
                
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend('Add Category', style={'color': 'green'}),
                                    dbc.Input(type='text', placeholder='New Category...', id='input-add-income', value=''),
                                    html.Br(),
                                    dbc.Button('Add', className='tbn btn-success', id='add-category-income', style={'margin-top': '20px'}),
                                    html.Br(),
                                    html.Div(id='category-div-add-income', style={}),
                                ], width=6),
                                
                                dbc.Col([
                                    html.Label('Remove categories', style={'color':'red'}),
                                    dbc.Checklist(
                                        id='checklist-selected-style-income',
                                        options=[{'label': i, 'value': i} for i in cat_income],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={"backgroundColor": "#fa7268",
                                                            "borderColor": "#ea6258"},
                                    ),
                                    dbc.Button('Remove', color='warning', id='remove-category-income', style={'margin-top': '20px'}),
                                ], width=6)
                            ]),
                        ], title='Add/Remove Categories',
                        ),
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
                    ], width=6)
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
                            switch=True),
                    ], width=4),
                    
                    dbc.Col([
                        html.Label('Expense Category'),
                        dbc.Select(id='select_expense', options=[{'label': i, 'value': i} for i in cat_expense])
                    ], width=4),
                ],style={"margin-top": "25px"}), 
                
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend('Add Category', style={'color': 'green'}),
                                    dbc.Input(type='text', placeholder='New Category...', id='input-add-expense', value=''),
                                    html.Br(),
                                    dbc.Button('Add', className='btn btn-success', id='add-category-expense', style={'margin-top': '20px'}),
                                    html.Br(),
                                    html.Div(id='category-div-add-expense', style={}),
                                ], width=6),
                                
                                dbc.Col([
                                    html.Label('Remove categories', style={'color':'red'}),
                                    dbc.Checklist(
                                        id='checklist-selected-style-expense',
                                        options=[{'label': i, 'value': i} for i in cat_expense],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={"backgroundColor": "#fa7268",
                                                    "borderColor": "#ea6258"},
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
    ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.QUARTZ})
], id='complete_sidebar')




#--Callbacks--#


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
        
        
# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("avatar_button", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open        
        
        
        
# Add/Remove expense category
@app.callback(
    [Output("category-div-add-expense", "children"),
    Output("category-div-add-expense", "style"),
    Output("select_expense", "options"),
    Output('checklist-selected-style-expense', 'options'),
    Output('checklist-selected-style-expense', 'value'),
    Output('stored-cat-expense', 'data')],

    [Input("add-category-expense", "n_clicks"),
    Input("remove-category-expense", 'n_clicks')],

    [State("input-add-expense", "value"),
    State('checklist-selected-style-expense', 'value'),
    State('stored-cat-expense', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_expense = list(data['Category'].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == '' or txt == None:
            txt1 = 'The text field cannot be empty to register a new category.'
            style1 = {'color': 'red'}

        else:
            cat_expense = cat_expense + [txt] if txt not in cat_expense else cat_expense
            txt1 = f'The Category {txt} was successfully added!'
            style1 = {'color': 'green'}
    
    if n2:
        if len(check_delete) > 0:
            cat_expense = [i for i in cat_expense if i not in check_delete]  
    
    opt_expense = [{"label": i, "value": i} for i in cat_expense]
    df_cat_expense = pd.DataFrame(cat_expense, columns=['Category'])
    df_cat_expense.to_csv("data/df_cat_expense.csv")
    data_return = df_cat_expense.to_dict()

    return [txt1, style1, opt_expense, opt_expense, [], data_return]
        
        
        
    # Add/Remove income category
@app.callback(
    [Output("category-div-add-income", "children"),
    Output("category-div-add-income", "style"),
    Output("select_income", "options"),
    Output('checklist-selected-style-income', 'options'),
    Output('checklist-selected-style-income', 'value'),
    Output('stored-cat-income', 'data')],

    [Input("add-category-income", "n_clicks"),
    Input("remove-category-income", 'n_clicks')],

    [State("input-add-income", "value"),
    State('checklist-selected-style-income', 'value'),
    State('stored-cat-income', 'data')]
)
def add_category(n, n2, txt, check_delete, data):
    cat_income = list(data["Category"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "The text field cannot be empty to register a new category."
            style1 = {'color': 'red'}

    if n and not(txt == "" or txt == None):
        cat_income = cat_income + [txt] if txt not in cat_income else cat_income
        txt1 = f'The Category {txt} was successfully added!'
        style1 = {'color': 'green'}
    
    if n2:
        if check_delete == []:
            pass
        else:
            cat_income = [i for i in cat_income if i not in check_delete]  
    
    opt_income = [{"label": i, "value": i} for i in cat_income]
    df_cat_income = pd.DataFrame(cat_income, columns=['Category'])
    df_cat_income.to_csv("data/df_cat_incomes.csv")
    data_return = df_cat_income.to_dict()

    return [txt1, style1, opt_income, opt_income, [], data_return]    
        
        
        
# Send income form
@app.callback(
    Output('store-income', 'data'),

    Input("save_income", "n_clicks"),

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

    if n and not(value == '' or value== None):
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

    Input("save_expense", "n_clicks"),

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

    if n and not(value == '' or value== None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        completed = 1 if 1 in switches else 0
        regular = 0 if 2 in switches else 0

        df_expenses.loc[df_expenses.shape[0]] = [value, completed, regular, date, category, description]
        df_expenses.to_csv("data/df_incomes.csv")

    data_return = df_expenses.to_dict()
    return data_return