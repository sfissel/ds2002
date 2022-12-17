#!/usr/bin/env python
# coding: utf-8

# # Extracting and Loading Data

# In[1]:


# import packages
import pandas as pd
import pymongo
import requests
import json


# # PART 1: Extract and Transform the Data

# In[2]:


# Extract data source into one Pandas dataframe:

## import relevant csv files as dataframes
best_movies = pd.read_csv("/Users/stephaniefissel/Desktop/ds2002/final project data/Best Movies Netflix.csv")
best_shows = pd.read_csv("/Users/stephaniefissel/Desktop/ds2002/final project data/Best Shows Netflix.csv")


# In[3]:


# Add dummy variables for movies and shows to distinguish type
best_movies['MOVIE_DUMMY'] = 1
best_movies['SHOW_DUMMY'] = 0
best_movies['NUMBER_OF_SEASONS'] = 0
best_shows['MOVIE_DUMMY'] = 0
best_shows['SHOW_DUMMY'] = 1


# In[4]:


# Concatenate dataframes with best movies and shows into Pandas dataframe
best = [best_movies, best_shows]
all = pd.concat(best, axis = 0, sort = False)
all = all.drop('index', axis=1)


# In[5]:


# Convert column variable integers to strings
all[['RELEASE_YEAR', 'SCORE', 'NUMBER_OF_VOTES', 'DURATION', 'MOVIE_DUMMY', 'SHOW_DUMMY', 'NUMBER_OF_SEASONS']] = all[['RELEASE_YEAR', 'SCORE', 'NUMBER_OF_VOTES', 'DURATION', 'MOVIE_DUMMY', 'SHOW_DUMMY', 'NUMBER_OF_SEASONS']].astype(str)
all.index = all.index.map(str)


# # PART 2: Load Data into MongoDB

# In[6]:


# Connect to MongoDB Instance

host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"


# In[7]:


conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
}

client = pymongo.MongoClient(conn_str["local"])

print(f"Local Connection String: {conn_str['local']}")


# In[8]:


# Assign database
db = client['Netflix']


# In[9]:


# Store in Mongo DB
db.collection.insert_many(all.to_dict('records'))

