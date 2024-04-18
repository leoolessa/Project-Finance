from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

import pdb
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO


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
                    html.H5('€ -', id='p-balance-dashboard', style={})
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
                    html.H5('€ -', id='p-income-dashboard', style={})
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
                    html.H5('€ -', id='p-expense-dashboard', style={})
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








# =========  Callbacks  =========== #
# Dropdown Income
@app.callback([Output("dropdown-income", "options"),
    Output("dropdown-income", "value"),
    Output("p-income-dashboards", "children")],
    Input("store-income", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    value = df['Value'].sum()
    val = df.Category.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Category.unique()]), val, f"R$ {value}"]

# Dropdown Expense
@app.callback([Output("dropdown-expense", "options"),
    Output("dropdown-expense", "value"),
    Output("p-expense-dashboards", "children")],
    Input("store-expense", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    value = df['Value'].sum()
    val = df.Category.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Category.unique()]), val, f"R$ {value}"]

# VALOR - balance
@app.callback(
    Output("p-balance-dashboards", "children"),
    [Input("store-expense", "data"),
    Input("store-income", "data")])
def saldo_total(expense, income):
    df_expense = pd.DataFrame(expense)
    df_income = pd.DataFrame(income)

    value = df_income['Value'].sum() - df_expense['Value'].sum()

    return f"R$ {value}"
    
# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-expense', 'data'),
    Input('store-income', 'data'),
    Input("dropdown-expense", "value"),
    Input("dropdown-income", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output(data_expense, data_income, expense, income, theme):
    df_ds = pd.DataFrame(data_expense).sort_values(by='Data', ascending=True)
    df_rc = pd.DataFrame(data_income).sort_values(by='Data', ascending=True)

    dfs = [df_ds, df_rc]
    for df in dfs:
        df['Accumulation'] = df['Value'].cumsum()
        df["Date"] = pd.to_datetime(df["Data"])
        df["Month"] = df["Date"].apply(lambda x: x.month)

    df_incomes_month = df_rc.groupby("Month")["Value"].sum()
    df_expenses_month = df_ds.groupby("Month")["Value"].sum()
    df_balance_month = df_incomes_month - df_expenses_month
    df_balance_month.to_frame()
    df_balance_month = df_balance_month.reset_index()
    df_balance_month['Accumulation'] = df_balance_month['Value'].cumsum()
    df_balance_month['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

    df_ds = df_ds[df_ds['Category'].isin(expense)]
    df_rc = df_rc[df_rc['Category'].isin(income)]

    fig = go.Figure()
    
    
    fig.add_trace(go.Scatter(name='Incomes', x=df_rc['Date'], y=df_rc['Accumulation'], fill='tonextx', mode='lines'))
   

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Gráfico 2
@app.callback(
    Output('graph2', 'figure'),
    [Input('store-income', 'data'),
    Input('store-expense', 'data'),
    Input('dropdown-income', 'value'),
    Input('dropdown-expense', 'value'),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]    
)
def graph2_show(data_expense, data_income, expense, income, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_expense)
    df_rc = pd.DataFrame(data_income)

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Incomes'
    df_ds['Output'] = 'Expenses'
    df_final = pd.concat(dfs)

    mask = (df_final['Date'] > start_date) & (df_final['Date'] <= end_date) 
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Category'].isin(income) | df_final['Category'].isin(expense)]

    fig = px.bar(df_final, x="Date", y="Value", color='Output', barmode="group")        
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig


# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-expense', 'data'),
    Input('dropdown-income', 'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_income(data_income, income, theme):
    df = pd.DataFrame(data_income)
    df = df[df['Category'].isin(income)]

    fig = px.pie(df, values=df.Value, names=df.Category, hole=.2)
    fig.update_layout(title={'text': "Incomes"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                  
    return fig    

# Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [Input('store-expense', 'data'),
    Input('dropdown-expense', 'value'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_expense(data_expense, expense, theme):
    df = pd.DataFrame(data_expense)
    df = df[df['Category'].isin(expense)]

    fig = px.pie(df, values=df.Value, names=df.Category, hole=.2)
    fig.update_layout(title={'text': "Expenses"})

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig