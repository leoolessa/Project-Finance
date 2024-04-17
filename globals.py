import pandas as pd
import os


if ('df_expenses.csv' in os.listdir()) and ('df_incomes.csv' in os.listdir()):
    df_expenses = pd.read_csv('df_expenses.csv', index_col=0, parse_dates=True)
    df_incomes = pd.read_csv('df_incomes.csv', index_col=0, parse_dates=True)
    
else:
    data_structure = {
        'Value':[],
        'Completed':[],
        'Regular':[],
        'Date':[],
        'Category':[],
        'Description':[],
    }
    df_expenses = pd.DataFrame(data_structure)    
    df_incomes = pd.DataFrame(data_structure)
    df_expenses.to_csv('data/df_expenses.csv')
    df_incomes.to_csv('data/df_incomes.csv')
    
    
if ('df_cat_expenses.csv' in os.listdir()) and ('df_cat_incomes.csv' in os.listdir()):
        df_cat_expenses = pd.read_csv('df_cat_expenses.csv', index_col=0)
        df_cat_incomes = pd.read_csv('df_cat_incomes.csv', index_col=0)
        cat_expense = df_cat_expenses.values.tolist()
        cat_income = df_cat_incomes.values.tolist()
else:
    cat_expense = {'Category': ['Rent', 'Bills', 'Supermarket', 'Wallet', 'Travels', 'Activities', 'Health']}
    cat_income = {'Category': ['Salary', 'Investments', 'Extra Earnings']}  
     
    df_cat_expenses = pd.DataFrame(cat_expense)
    df_cat_incomes = pd.DataFrame(cat_income) 
    df_cat_expenses.to_csv('data/df_cat_expenses.csv')
    df_cat_incomes.to_csv('data/df_cat_incomes.csv')   