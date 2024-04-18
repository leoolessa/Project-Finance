import pandas as pd
import os


if ('data/df_expenses.csv' in os.listdir()) and ('data/df_incomes.csv' in os.listdir()):
    df_expenses = pd.read_csv('data/df_expenses.csv', index_col=0, parse_dates=True)
    df_incomes = pd.read_csv('data/df_incomes.csv', index_col=0, parse_dates=True)
    df_incomes.info()
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
    
    
if ('data/df_cat_expense.csv' in os.listdir()) and ('data/df_cat_income.csv' in os.listdir()):
        df_cat_expense = pd.read_csv('data/df_cat_expense.csv', index_col=0)
        df_cat_income = pd.read_csv('data/df_cat_income.csv', index_col=0)
        cat_expense = df_cat_expense.values.tolist()
        cat_income = df_cat_income.values.tolist()

else:
    cat_expense = {'Category': ['Rent', 'Bills', 'Supermarket', 'Wallet', 'Travels', 'Activities', 'Health']}
    cat_income = {'Category': ['Salary', 'Investments', 'Extra Earnings']}  
     
    df_cat_expense = pd.DataFrame(cat_expense, columns=['Category'])
    df_cat_income = pd.DataFrame(cat_income, columns=['Category']) 
    df_cat_expense.to_csv('data/df_cat_expense.csv')
    df_cat_income.to_csv('data/df_cat_income.csv')   