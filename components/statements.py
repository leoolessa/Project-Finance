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


# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('expenses-table', 'children'),
    Input('store-expenses', 'data')
)
def print_table (data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    df.loc[df['Completed'] == 0, 'Completed'] = 'No'
    df.loc[df['Completed'] == 1, 'Completed'] = 'Yes'

    df.loc[df['Regular'] == 0, 'Regular'] = 'No'
    df.loc[df['Regular'] == 1, 'Regular'] = 'Yes'

    df = df.fillna('-')

    df.sort_values(by='Data', ascending=False)

    table = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Description" or i == "Regular" or i == "Completed"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return table

# Bar Graph            
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-expenses', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart(data, theme):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Category").sum()[["Value"]].reset_index()
    graph = px.bar(df_grouped, x='Category', y='Value', title="General Expenses")
    graph.update_layout(template=template_from_url(theme))
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph

# Simple card
@app.callback(
    Output('expense_value_card', 'children'),
    Input('store-expenses', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    value = df['Value'].sum()
    
    return f"€ {value}"