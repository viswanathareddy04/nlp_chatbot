# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:51:15 2022

@author: injav
"""

import logging
import sys
import yaml
import pandas as pd
import nltk
import numpy as np
import string
import warnings
import requests
import pickle
import random
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler, CallbackContext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression


studentid =""

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def response(user_response):
    text_test = [user_response]
    X_test = vectorizer.transform(text_test)
    prediction = lr.predict(X_test)
    reply = random.choice(responses[prediction[0]]['response'])
    return reply

# To get indent
def intent(user_response):
    text_intent = [user_response]
    X_test_intent = vectorizer.transform(text_intent)
    predicted_intent = lr.predict(X_test_intent)
    intent_predicted =responses[predicted_intent[0]]['intent']
    return intent_predicted



def bot_initialize(update, context):
    user_msg = update.message.text
    print(user_msg)
    flag=True
    while(flag==True):
        user_response = user_msg
        
        user_intent = intent(user_response)
        
        if(user_intent != 'goodbye' or user_intent != 'studentid' ):
            if(user_response == '/start'):
                resp = """Hi! Here is what I can do!!! 1. I can give you your Grades \n 2. College Fee \n  3. Exam Dates.\n\n 4. or Type Bye to Exit."""
                update.message.reply_text(resp)
                return

            elif (user_intent == 'greetings'):
                resp = str(random.choice(responses[0]['response'])) + ", Before we start, can I get your student ID please? ex: C0XXXXXX"
                update.message.reply_text(resp)
                return
            
            if (user_intent == 'studentid'):
                resp = str(random.choice(responses[1]['response'])) + userDict.get(user_msg,default="C01")
                studentid = userDict.get(user_msg,default="C01")
                update.message.reply_text(resp)
                return
        
            elif(user_intent == 'thankyou'):
                resp = random.choice(responses[10]['response'])
                update.message.reply_text(resp)
                return
            
            elif(user_intent == 'availability'):
                resp = random.choice(responses[1]['response'])
                update.message.reply_text(resp)
                return
            
            elif(user_intent == "flowers"):
                user_response=user_response.lower()
                resp = "I will suggest you to give :-\n " + response(user_response)
                update.message.reply_text(resp)
                return
            
            else:
                resp = "Ummm! Please rephrase your sentence. I am not that smart."
                update.message.reply_text(resp)
                return
            
        else:
            flag = False
            resp = random.choice(responses[9]['response'])
            update.message.reply_text(resp)
            return
    

def main():
    updater = Updater(config['telegram']['token'], use_context=True)
    disp = updater.dispatcher
    disp.add_handler(MessageHandler(Filters.text, bot_initialize))
    updater.start_polling()
    updater.idle()




if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level =logging.INFO)
    userDict = {
        "C01": "John",
        "C02": "Dan",
        "C03": "Michelle",
        "C04": "Rosi"
    }
    data = [["Hi",0],["Hello",0],["Hey",0],["Heya",0],
        ["C02",1],["C01",1],["C03",1],["C04",1],
        ["Suggest for birthday",2],["For Birthday",2],["I want some flowers for Birthday",2],["What type of flowers to give on Birthday?",2],["Suggest something for Birthday",2],["I want to give it to someone for Birthday",2],        
        ["Suggest for anniversary",3],["For Anniversary",3],["I want some flowers for Anniversary",3],["What type of flowers to give on Anniversary?",3],["Suggest something for Anniversary",3],["I want to give it to someone for Anniversary",3],
        ["Suggest for congratulations",4],["For Congratulations",4],["I want some flowers for Congratulating someone",4],["What type of flowers to give for Congratulations?",4],["Suggest something for Congratulations",4],["I want to give it to someone for Congratulating them",4],
        ["Suggest for wedding",5],["For Wedding",5],["I want some flowers for Wedding",5],["What type of flowers to give on Wedding?",5],["Suggest something for Wedding",5],["I want to give it to someone for Wedding",5],
        ["Suggest for sorry",6],["For Sorry",6],["I want some flowers for saying Sorry",6],["What type of flowers to give for saying Sorry?",6],["Suggest something for saying Sorry",6],["I want to give it to someone for saying Sorry",6],
        ["Suggest for miss you",7],["For Miss You",7],["Missing Someone",7],["I want some flowers for Miss You",7],["What type of flowers to give on Miss You?",7],["Suggest something for Miss You",7],["I want to give it to someone for Miss You",7],
        ["Suggest for get well soon",8],["For Get Well Soon",8],["I want some flowers for Get Well Soon",8],["What type of flowers to give for Get Well Soon?",8],["Suggest something for Get Well Soon",8],["I want to give it to someone for Get Well Soon",8],
        ["Goodbye",9],["Byebye",9],["Bye",9],
        ["Thanku",10],["Thank You",10],["Thanks",10],["Thanks a lot",10],["Thank you very much",10],["Thank you so much",10]]




    responses = {0 : {"intent":"greetings","response":['Hi Dear','Hi','Hello', 'Nice to see you',]}, 
      1 : {"intent":"studentid","response":['Welcome to Lambton',]},
      2 : {"intent":"flowers","response":['Endearing Red Roses','Sunshine Yellow Roses','Extravagant 40 Red Roses']},
      3 : {"intent":"flowers","response":['Lillies & Roses Elegant','15 Regal Carnations','Purple Orchids']},
      4 : {"intent":"flowers","response":['Purple Orchids','Yellow Asiatic Lillies','Dark Pink Roses']},
      5 : {"intent":"flowers","response":['Vivid Red Roses','Sweet Pink Roses','12 Purple Orchids']},
      6 : {"intent":"flowers","response":['Pure Love Carnations','Majestic 18 white Roses','Multicolour Roses']},
      7 : {"intent":"flowers","response":['White N Red Floral Beauty','Red Carnation N Leaves','Admirable Asiatic Pink Lillies']},
      8 : {"intent":"flowers","response":['Mesmerizing Charm','Serene Carnation','Unending Love 18 Light Pink Flowers']},
      9 : {"intent":"goodbye","response":['Goodbye','Byebye','Bye','Have a good day']},
      10 : {"intent":"thankyou","response":['You\'re welcome.' , 'No problem.', 'No worries.', ' My pleasure.' , 'Glad to help.']}}


    with open('application-config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    df = pd.DataFrame(data, columns = ["Text","Intent"])
    lemmer = nltk.stem.WordNetLemmatizer()
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    x = df['Text']
    y = df['Intent']
    vectorizer = TfidfVectorizer(tokenizer=Normalize,stop_words = 'english')
    X = vectorizer.fit_transform(x)
    lr = LogisticRegression()
    lr.fit(X, y) 
    X_test = ["flowers"]
    prediction = lr.predict(vectorizer.transform(X_test))
    lr.predict_proba(vectorizer.transform(X_test))
    main()