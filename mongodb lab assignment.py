#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import requests
import pandas as pd
import pgeocode
from bs4 import BeautifulSoup
import pymongo


# In[3]:


# Ask user for zip code as input
zip_code = input()


# In[4]:


# Use pgeocode library for GPS coordinates
nomi = pgeocode.Nominatim('us')
zipc = nomi.query_postal_code(zip_code)
zipc


# In[5]:


# Get latitude and longitude values from zip code data
latitude = zipc[9]
longitude = zipc[10]
print (latitude, longitude)


# In[6]:


urlQuote = 'https://forecast.weather.gov/MapClick.php'
querystring = {"lat": latitude,
               "lon": longitude}
print(querystring)


# In[7]:


header_var ={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# In[8]:


response = requests.request("GET",urlQuote,headers=header_var,params=querystring)


# In[9]:


# Insert latitude and longitude into url
print(response.url)
print(response.status_code)


# In[10]:


# Scrape 7 day forecast


# In[11]:


page = requests.get(response.url)
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())


# In[12]:


period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
print(period)
print(short_desc)
print(temp)


# In[13]:


img = tonight.find("img")
desc = img['title']
print(desc)


# In[14]:


period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
periods


# In[15]:


short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(short_descs)
print (temps)
print(descs)


# In[16]:


# 7-day forecast
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})
# convert index int to string
weather.index = weather.index.map(str)
weather


# In[ ]:


# Display current conditions 


# In[17]:


page = requests.get(response.url)
soup = BeautifulSoup(page.content, 'html.parser')


# In[18]:


humidity = soup.find_all('td')[1].get_text()
humidity


# In[19]:


windspeed = soup.find_all('td')[3].get_text()
windspeed


# In[20]:


dewpoint = soup.find_all('td')[7].get_text()
dewpoint


# In[21]:


time = soup.find_all('td')[13].get_text()
time


# In[22]:


# Current conditions
current_weather = pd.DataFrame({
    "Humidity": [humidity],
    "Wind Speed": [windspeed],
    "Dewpoint": [dewpoint],
    "Last Update Time": [time]
})
# convert index int to string
current_weather.index = current_weather.index.map(str)
current_weather


# In[23]:


# Storing in MongoDB


# In[24]:


#Connect to MongoDB Instance
host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"


# In[25]:


conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
}

client = pymongo.MongoClient(conn_str["local"])

print(f"Local Connection String: {conn_str['local']}")


# In[26]:


# Convert weather dataframe to dictionary
w_dict = weather.to_dict()
print(w_dict)


# In[27]:


# Assign database
db = client['Weather']


# In[28]:


# Assign collection
collection = db['7-Day Forecast']


# In[29]:


# Store in MongoDB
collection.insert_one(w_dict)


# In[30]:


# Convert current weather dataframe to dictionary 
cw_dict = current_weather.to_dict()
print(cw_dict)


# In[31]:


# Assign database
db = client['Weather']


# In[32]:


# Assign collection
collection = db['Current Conditions']


# In[33]:


# Store in MongoDB
collection.insert_one(cw_dict)


# In[ ]:




