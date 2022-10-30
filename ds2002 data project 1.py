#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import csv
import requests
import pandas as pd
import sqlite3


# In[4]:


## Fetching remote data file by URL
# import urllib library
from urllib.request import urlopen
# store URL in url as parameter for urlopen
url = "https://holidays.abstractapi.com/v1/?api_key=574b7d06a79c4794a2e390123a19b857&country=US&year=2020"
# store the response of URL
response = urlopen(url)
#storing the JSON response from url in data
data_json = json.loads(response.read())
# print the json response
print(data_json)


# In[5]:


# Converting from JSON to SQLite database (with reduced number of columns from source to destination)
api_url = requests.get('https://holidays.abstractapi.com/v1/?api_key=574b7d06a79c4794a2e390123a19b857&country=US&year=2020')
data_json = api_url.json()

connection = sqlite3.connect('holiday.sqlite')
cursor = connection.cursor()
cursor.execute('Create Table if not exists holiday (name TEXT, date TEXT, type TEXT, country TEXT)')

columns = ['name','date','type', 'country']
for row in data_json:
    keys= tuple(row[c] for c in columns)
    cursor.execute('insert into holiday values(?,?,?,?)',keys)
    print(f'{row["name"]} data inserted Succefully')

connection.commit()
connection.close()


# In[6]:


# Producing informative error if file doesn't exist to save
try:
    with open('holiday.sqlite') as file:
        print("File present")
except FileNotFoundError:
    print('File is not present')


# In[7]:


# Converting from JSON to CSV (local file) written to disk
data = pd.read_json('https://holidays.abstractapi.com/v1/?api_key=574b7d06a79c4794a2e390123a19b857&country=US&year=2020')
data.to_csv('holiday.csv', index=None)


# In[8]:


# Modifying number of columns from source to destination: CSV file
## Removing columns: date_day, date_month, date_year, description, language, location, name_local
data.drop(['date', 'description', 'language', 'location', 'name_local'], inplace=True, axis=1)


# In[9]:


## Adding date column that combines weekday, date day, month, and year of holiday
data["date"] = (data["week_day"].astype(str) + " " + data["date_month"].astype(str) + "/" + data["date_day"].astype(str) + "/" + data["date_year"].astype(str))
data.drop(['date_day', 'date_month', 'date_year', 'week_day'], inplace=True, axis=1)


# In[10]:


## Reordering columns
data = data[['name', 'date', 'type', 'country']]


# In[11]:


## Updating new CSV file written to disk (local file)
data.to_csv('holiday.csv', index=None)


# In[12]:


# Producing informative error if file doesn't exist to update
try:
    with open('holiday.csv') as file:
        read_data = file.read()
except FileNotFoundError as fnf_error:
    print(fnf_error)


# In[13]:


# Brief summary of data file ingestion for SQLite database
import sqlite3

# Connecting to sqlite
# connection object
connection_obj = sqlite3.connect('holiday.sqlite')

# cursor object
cursor_obj = connection_obj.cursor()

print("Number of Records: ")
cursor_obj.execute("SELECT * FROM HOLIDAY")
print(len(cursor_obj.fetchall()))

print("Number of Columns: ")
cursor_obj.execute("SELECT * FROM pragma_table_info('HOLIDAY')")
print(len(cursor_obj.fetchall()))

# Close the connection
connection_obj.close()


# In[14]:


# Brief summary of data file ingestion for CSV file
total_records = len(data.axes[0])
total_columns = len(data.axes[1])
print("Number of Records: "+ str(total_records))
print("Number of Columns: "+ str(total_columns))


# In[ ]:




