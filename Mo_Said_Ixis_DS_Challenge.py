#!/usr/bin/env python
# coding: utf-8

# IXIS Data Science Challenge - Online Retailer Performance Analysis
# 
# Mohammed Said

# In[2]:


#Install and import the necessary packages
get_ipython().system('pip install -r requirements.txt')
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib as plt
import seaborn as sns


# In[ ]:


#Using this to make the future decimals more readable
pd.options.display.float_format = '{:.5f}'.format


# In[ ]:


#Lets read the csv files into a Pandas dataframe and store it as generic named variables


# In[ ]:


sessioncountsdf = pd.read_csv("DataAnalyst_Ecom_data_sessionCounts.csv")


# In[ ]:


addstocartdf = pd.read_csv("DataAnalyst_Ecom_data_addsToCart.csv")


# In[ ]:


#Data Exploration and wrangling


# In[ ]:


sessioncountsdf.head()


# In[ ]:


sessioncountsdf.describe()


# In[ ]:


sessioncountsdf.info()


# In[ ]:


#No null found in this dataset
sessioncountsdf.isnull().sum()


# In[ ]:


# The below column needs to be converted to datetime datatype

sessioncountsdf.dim_date = pd.to_datetime(sessioncountsdf.dim_date)



# In[ ]:


#Lets look at categorizing/cleaning some columns
sessioncountsdf.dim_browser.unique()


# In[ ]:


#We have quite a decent amount of 'error' values and (not set) values
sessioncountsdf.dim_browser.value_counts()


# In[ ]:


sessioncountsdf.query('dim_browser=="error"')


# In[ ]:


sessioncountsdf.query('dim_browser=="error"').describe()


# In[ ]:


sessioncountsdf.query('dim_browser=="(not set)"')


# In[ ]:


sessioncountsdf.query('dim_browser=="(not set)"').describe()


# In[ ]:


sessioncountsdf


# In[ ]:


#I considered keeping rows with values 'error' and '(not set') but I believe they are insignificant for our analysis with the logic being their transactions and QTY are zero anyways so they serve minimal purpose
#We will drop rows containing those values

sessioncountsdf = sessioncountsdf[(sessioncountsdf.dim_browser != "(not set)") & (sessioncountsdf.dim_browser != "error")]


# In[ ]:


#Lets also convert this column to Category data type

sessioncountsdf.dim_deviceCategory = sessioncountsdf.dim_deviceCategory.astype("category")


# In[ ]:


sessioncountsdf.info()


# In[ ]:


sessioncountsdf.dim_deviceCategory.value_counts()


# In[ ]:


sessioncountsdf.describe()


# Moving on to the second dataframe

# In[ ]:


addstocartdf.head()


# In[ ]:


#No nulls found in this dataset
addstocartdf.isnull().sum()


# In[ ]:


addstocartdf.info()


# In[ ]:


addstocartdf.describe()


# Deliverables:

# In[ ]:


#Creating a copy of the first dataset that we will eventually turn into the First Sheet
df1 = sessioncountsdf.copy()


# In[ ]:


df1


# In[ ]:


#Creating the column for month
df1['month'] = df1['dim_date'].dt.strftime('%Y-%m')


# In[ ]:


df1 = df1.groupby(['month','dim_deviceCategory']).sum().reset_index()


# In[ ]:


#Creating the column for ECR calculated by Transactions divided by Sessions
df1['ECR'] = (df1['transactions'] / df1['sessions'])


# In[ ]:


df1.info()


# In[ ]:


df1.head(5)


# Let's plot some interactive graphs for the variables

# In[ ]:


fig1 = px.line(df1, x="month", y="transactions", color="dim_deviceCategory", title="Transactions vs Month of the year")
fig1.update_layout(
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend_title_text="Device Category",

    )
fig1.show()


# In[ ]:


fig2 = px.line(df1, x="month", y="sessions", color="dim_deviceCategory", title="Sessions vs Month of the year")
fig2.update_layout(
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend_title_text="Device Category",

    )
fig2.show()


# In[ ]:


fig3 = px.line(df1, x="month", y="QTY", color="dim_deviceCategory", title="QTY vs Month of the year")
fig3.update_layout(
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend_title_text="Device Category",

    )
fig3.show()


# In[ ]:


fig4 = px.line(df1, x="month", y="ECR", color="dim_deviceCategory", title="ECR vs Month of the year")
fig4.update_layout(
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend_title_text="Device Category",

    )
fig4.show()


# In[ ]:


#Checking for correlation between the columns
df1.corr()


# In[ ]:


#Lets group the dataframe and rename these columns so they look prettier before we export to xlsx
df1.rename(columns= {'months':'Month','dim_deviceCategory':'Device_Category','sessions':'Sessions', 'transactions':'Transactions'}, inplace=True)


# In[ ]:


#Lets group the dataframe and rename these columns so they look prettier before we export to xlsx
df1.rename(columns= {'months':'Month','dim_deviceCategory':'Device_Category','sessions':'Sessions', 'transactions':'Transactions'}, inplace=True)


# In[ ]:


firstsheet = df1.groupby(['month','Device_Category']).sum()


# In[ ]:


#Exporting firstsheet to xlsx
firstsheet.to_excel(r'firstsheet.xlsx', index=True, header=True)


# In[ ]:


##Creating a copy of the second dataset that we will eventually turn into the Second Sheet
df2 = addstocartdf.copy()


# Moving on to the second sheet
# 

# In[ ]:


#Lets review the dataset
df2.head()


# In[ ]:


#Creating a new column for month that matches the other dataset
df2['month'] = df2[['dim_year', 'dim_month']].astype(str).agg('-'.join, axis=1)


# In[ ]:


df2


# In[ ]:


#Converting the new month column to datetime data type to match df1 in anticipation of merge
df2['month'] = pd.to_datetime(df2['month'])


# In[ ]:


#Matching the new month column to month column in df1 so plotly can accept and plot values
df2['month'] = df2['month'].dt.strftime('%Y-%m')


# In[ ]:


#Dropping the original year and month columns
df2 = df2.drop(["dim_year","dim_month"], axis=1)


# In[ ]:


#Rearranging year_month to be first column
firstcolumn = df2.pop('month')


# In[ ]:


df2.insert(0,'month', firstcolumn)


# In[ ]:


df2


# In[ ]:


df2.describe()


# In[ ]:


fig5 = px.line(df2, x="month", y="addsToCart", title="AddsToCart vs Month of the year")
fig5.update_layout(
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}

    )
fig5.show()


# In[ ]:


df2


# In[ ]:


#Merging the two dataset by the month column
mergeddf = pd.merge(df1,df2, how='left', left_on=['month'], right_on=['month'])


# In[ ]:


mergeddf


# In[ ]:


mergeddf.corr()


# In[ ]:


#Storing the merged dataframe in a variable named secondsheet
secondsheet = mergeddf.groupby('month').sum()


# In[ ]:


secondsheet


# In[ ]:


#Restructuring secondsheet with only the last two months data
secondsheet = secondsheet.iloc[-2:]


# In[ ]:


#Calculating the absolute difference between the two months
absolutedifference = secondsheet.diff().dropna()


# In[ ]:


#Calculating the relative difference between the two months
relativedifference = ((absolutedifference/ secondsheet.iloc[-2]))


# In[ ]:


#Adding the absolute  difference to the secondsheet dataframe
secondsheet = secondsheet.append(absolutedifference)


# In[ ]:


#Adding the relative difference to the secondsheet dataframe
secondsheet = secondsheet.append(relativedifference)


# In[ ]:


#Naming the column and filling in the rows appropriately
secondsheet['difference'] = [" ", " ", "Absolute", "Relative"]


# In[ ]:


#Resetting the index for better view
secondsheet = secondsheet.reset_index()


# In[ ]:


#Removing the month values for the fields containing the absolute and relative difference
secondsheet['month'].iloc[-2:] = " "


# In[ ]:


secondsheet


# In[ ]:


#Saving the secondsheet into an xlsx
secondsheet.to_excel(r'secondsheet.xlsx', index=False, header=True)


# In[ ]:




