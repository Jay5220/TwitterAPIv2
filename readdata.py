# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:15:13 2022

@author: nguye
"""

import pandas as pd
import dateutil.parser
import numpy as np
import statsmodels.api as sm
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('data.csv')
num1 = df

column_names = ['mean_likes', 'mean_retweets', 'mean_quotes', 'mean_replies', 'max_likes', 'max_retweets', 'max_quotes','max_replies', 'num_tweets' , 'Date']


data_dict = {}

for index, row in df.iterrows():
    if row['like_count']>0 or row['retweet_count']>0 or row['quote_count']>0 or row['reply_count']>0:
        #get the date
        date = dateutil.parser.parse(row['created_at']).day
        
        #create a new array for each date
        if date not in data_dict:
            data_dict[date] = [0] * 10
        
        #add the likes
        data_dict[date][0] = data_dict[date][0] + row['like_count']
        if data_dict[date][4] < row['like_count']:
            data_dict[date][4] = row['like_count']
        
        #add the retweets
        data_dict[date][1] = data_dict[date][1] + row['retweet_count']
        if data_dict[date][5] < row['retweet_count']:
            data_dict[date][5] = row['retweet_count']
        
        #add the quotes
        data_dict[date][2] = data_dict[date][2] + row['quote_count']
        if data_dict[date][6] < row['quote_count']:
            data_dict[date][6] = row['quote_count']
        
        #add the replies
        data_dict[date][3] = data_dict[date][3] + row['reply_count']
        if data_dict[date][7] < row['reply_count']:
            data_dict[date][7] = row['reply_count']
        
        data_dict[date][8] = data_dict[date][8]+1
        
        data_dict[date][9] = date


for date in data_dict:
    data_dict[date][0] = data_dict[date][0]/data_dict[date][8]
    data_dict[date][1] = data_dict[date][1]/data_dict[date][8]
    data_dict[date][2] = data_dict[date][2]/data_dict[date][8]
    data_dict[date][3] = data_dict[date][3]/data_dict[date][8]

new_df = pd.DataFrame.from_dict(data_dict, orient='index',columns = column_names)

sales = pd.read_csv('sales.csv')

new_df = new_df.set_index('Date').join(sales.set_index('Date'))
print(new_df)

X = new_df[['mean_likes','mean_retweets','max_retweets', 'max_replies', 'num_tweets']]
Y1 = new_df[['Number of sales']]
Y2 = new_df[['Sales USD']]
X = sm.add_constant(X)
model1 = sm.OLS(Y1,X)
results1 = model1.fit()
print(results1.summary())
model2 = sm.OLS(Y2,X)
results2 = model2.fit()
print(results2.summary())

A = new_df[['Number of sales', 'Sales USD']]
B = new_df[['num_tweets']]
model3 = sm.OLS(B,A)
results3 = model3.fit()
print(results3.summary())

