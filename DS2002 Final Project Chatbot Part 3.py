#!/usr/bin/env python
# coding: utf-8

# # PART 3: Running the bot to answer questions

# In[1]:


import pymongo
from pymongo import MongoClient


# In[2]:


# pip install tensorflow


# In[3]:


import nltk 
import discord
nltk.download('punkt')


# In[4]:


from nltk import word_tokenize,sent_tokenize


# In[5]:


from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np 
import tflearn
import tensorflow as tf
import random
import json
import pickle


# In[ ]:


# connect to db and read in intent collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Netflix"]
mycol = mydb["collection"]

with open("/Users/stephaniefissel/Desktop/ds2002/intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in ai_intents.find():
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)



def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question1:
                    query1 = mycol.find({"MAIN_GENRE": "romance", "MOVIE_DUMMY": "1"}).sort("SCORE",-1).limit(3)
            print("The top three rated romance movies on Netflix are:")
            for x in query1:
                print(x)
            
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question2:
                    query2 = mycol.find({"MOVIE_DUMMY": "1"}).sort("DURATION", -1).limit(1)
            print("The longest top movie on Netflix is:")
            for x in query2:
                print(x)
        
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question3:
                    query3 = mycol.find({"RELEASE_YEAR": "2001"}).sort("SCORE",-1).limit(1)
            print("The genre of the top movie in 2001 is:")
            for x in query3:
                print(x)
            
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question4:
                    query4 = mycol.find({"MOVIE_DUMMY":"1", "MAIN_GENRE": "drama", "SCORE":{"$gte":"8"}})
            print("These were the drama movies with a score greater than or equal to 8:")
            for x in query4:
                print(x)
            
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question5:
                    query5 = mycol.find({"MOVIE_DUMMY":"1", "MAIN_PRODUCTION": "GB"})
            print("These were the movies that were mainly produced in GB:")
            for x in query5:
                print(x)
            
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question6:
                    query6 = mycol.find({"SHOW_DUMMY":"1", "RELEASE_YEAR": {"$lt":"2000"}})
            print("These were the top shows on Netflix produced before 2000:")
            for x in query6:
                print(x)
            
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question7:
                    query7 = mycol.find({"SHOW_DUMMY":"1", "RELEASE_YEAR": "2017"}).sort("SCORE", -1).limit(1)
            print("This was the top show on Netflix 5 years ago:")
            for x in query7:
                print(x)
        
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question8:
                    query8 = mycol.find({"SHOW_DUMMY":"1"}).sort("NUMBER_OF_SEASONS", -1).limit(1)
            print("This was the top show on Netflix with the most seasons:")
            for x in query8:
                print(x)
                
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question9:
                    query9 = mycol.find({"SHOW_DUMMY":"1"}).sort("NUMBER_OF_VOTES", -1).limit(1)
            print("This was the show that received the most votes:")
            for x in query9:
                print(x)
                
        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == question10:
                    query10 = mycol.find({"MOVIE_DUMMY":"1"}).sort("SCORE", -1).limit(1)
            print("This is the top movie on Netflix with the highest score:")
            for x in query10:
                print(x)

        else:
            print("I didnt get that. Try again with one of these 10 questions: What were the top three rated romance movies on Netflix of all time?, What was the longest top movie on Netflix?, What was the genre of the top movie in 2001?, What drama movies have a score greater than or equal to 8?, What movies were mainly produced in GB?, What top shows on Netflix were produced before 2000?, What was the top show on Netflix 5 years ago?, What show has the most seasons?, What show has received the most votes? What is the top movie on Netflix with the highest score?")
chat()


# In[ ]:




