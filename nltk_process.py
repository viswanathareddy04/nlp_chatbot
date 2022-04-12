# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:10:28 2022

@author: Group 4
"""
import random
import string

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from bot_responses import BotResponses


class NLTKProcess:
    lr = LogisticRegression()
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    lemmer = nltk.stem.WordNetLemmatizer()
    botResponse = BotResponses()

    def __init__(self):
        self._vectorizer = TfidfVectorizer(tokenizer=self.Normalize, stop_words='english')

    def performLogisticRegression(self, dataset):
        x = dataset['Text']
        y = dataset['Intent']
        X = self._vectorizer.fit_transform(x)
        self.lr.fit(X, y)
        X_test = ["exam"]
        prediction = self.lr.predict(self._vectorizer.transform(X_test))
        self.lr.predict_proba(self._vectorizer.transform(X_test))

    def LemTokens(self, tokens):
        for token in tokens:
            return self.lemmer.lemmatize(token)

    def Normalize(self, text):
        word_tokenize = nltk.word_tokenize(text.lower().translate(self.remove_punct_dict))
        return self.LemTokens(word_tokenize)

    def response(self, user_response):
        text_test = [user_response]
        X_test = self._vectorizer.transform(text_test)
        prediction = self.lr.predict(X_test)
        reply = random.choice(self.botResponse.responses[prediction[0]]['response'])
        return reply

    # To get intent
    def intent(self, user_request):
        text_intent = [user_request]
        X_test_intent = self._vectorizer.transform(text_intent)
        predicted_intent = self.lr.predict(X_test_intent)
        intent_predicted = self.botResponse.responses[predicted_intent[0]]['intent']
        return intent_predicted


NLTK_Process = NLTKProcess()
