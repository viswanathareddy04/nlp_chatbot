# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:51:15 2022

@author: injav
"""

import logging
import random
import string
import sys

import nltk
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from telegram.ext import Updater, MessageHandler, Filters

student_id = ''

student_information = {
    "C01": {
        "name": "John",
        "exam": "April 14, 2022",
        "grades": "CBD: 89%\nALML:95%",
        "fee": "$200"
    },
    "C02": {
        "name": "Dan",
        "exam": "April 14, 2022",
        "grades": "CBD: 90%\nALML:95%",
        "fee": "$100"
    },
    "C03": {
        "name": "Michelle",
        "exam": "April 14, 2022",
        "grades": "CBD: 79%\nALML:95%",
        "fee": "$150"
    },
    "C04": {
        "name": "Rosi",
        "exam": "April 14, 2022",
        "grades": "CBD: 84%\nALML:95%",
        "fee": "$230"
    }
}


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
    intent_predicted = responses[predicted_intent[0]]['intent']
    return intent_predicted


def bot_initialize(update, context):
    global student_id
    student_info = student_information.get(student_id) or {}
    user_msg = update.message.text
    print(user_msg)
    flag = True
    while flag:
        user_response = user_msg

        user_intent = intent(user_response)

        if user_intent != 'goodbye':
            if user_response.lower().startswith('c0'):
                student_id = user_response or 'C01'
                resp = str(random.choice(responses[1]['response'])).format(
                    username=student_information.get(student_id, {}).get('name'))
                what_we_do = """Hi! Here is what I can do!!! \n1. I can give you your Grades\n2. College Fee\n3. Exam Dates.\n\n4. or Type goodbye to Exit."""
                update.message.reply_text(resp + '\n' + what_we_do)
                return

            if user_response == '/start' or not student_id:
                resp = str(random.choice(
                    responses[0]['response'])) + ", Before we start, can I get your student ID please? ex: C0XXXXXX"
                update.message.reply_text(resp)
                return

            if user_intent == "grade":
                resp = str(random.choice(responses[11]['response'])).format(username=student_info.get('name'),
                                                                            grades=student_info.get('grades'))
                update.message.reply_text(resp)
                return

            if user_intent == "fee":
                resp = str(random.choice(responses[12]['response'])).format(username=student_info.get('name'),
                                                                            college_fee=student_info.get('fee'))
                update.message.reply_text(resp)
                return

            if user_intent == "date":
                resp = str(random.choice(responses[13]['response'])).format(username=student_info.get('name'),
                                                                            exam_date=student_info.get('exam'))
                update.message.reply_text(resp)
                return

            if user_intent == 'thankyou':
                resp = random.choice(responses[10]['response'])
                update.message.reply_text(resp)
                return

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
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    data = [
        ["Hi", 0], ["Hello", 0], ["Hey", 0], ["Heya", 0],
        ["Suggest for birthday", 2], ["For Birthday", 2], ["I want some flowers for Birthday", 2],
        ["What type of flowers to give on Birthday?", 2], ["Suggest something for Birthday", 2],
        ["I want to give it to someone for Birthday", 2],
        ["Suggest for anniversary", 3], ["For Anniversary", 3], ["I want some flowers for Anniversary", 3],
        ["What type of flowers to give on Anniversary?", 3], ["Suggest something for Anniversary", 3],
        ["I want to give it to someone for Anniversary", 3],
        ["Suggest for congratulations", 4], ["For Congratulations", 4],
        ["I want some flowers for Congratulating someone", 4],
        ["What type of flowers to give for Congratulations?", 4], ["Suggest something for Congratulations", 4],
        ["I want to give it to someone for Congratulating them", 4],
        ["Suggest for wedding", 5], ["For Wedding", 5], ["I want some flowers for Wedding", 5],
        ["What type of flowers to give on Wedding?", 5], ["Suggest something for Wedding", 5],
        ["I want to give it to someone for Wedding", 5],
        ["Suggest for sorry", 6], ["For Sorry", 6], ["I want some flowers for saying Sorry", 6],
        ["What type of flowers to give for saying Sorry?", 6], ["Suggest something for saying Sorry", 6],
        ["I want to give it to someone for saying Sorry", 6],
        ["Suggest for miss you", 7], ["For Miss You", 7], ["Missing Someone", 7],
        ["I want some flowers for Miss You", 7], ["What type of flowers to give on Miss You?", 7],
        ["Suggest something for Miss You", 7], ["I want to give it to someone for Miss You", 7],
        ["Suggest for get well soon", 8], ["For Get Well Soon", 8], ["I want some flowers for Get Well Soon", 8],
        ["What type of flowers to give for Get Well Soon?", 8], ["Suggest something for Get Well Soon", 8],
        ["I want to give it to someone for Get Well Soon", 8],
        ["Goodbye", 9], ["Byebye", 9], ["Bye", 9],
        ["Thanku", 10], ["Thank You", 10], ["Thanks", 10], ["Thanks a lot", 10], ["Thank you very much", 10],
        ["Thank you so much", 10],
        ["grade", 11], ['grades', 11], ['marks', 11],
        ["fee", 12], ['college fee', 12], ['semester fee', 12],
        ["date", 13], ['exam date', 13], ['semester date', 13]
    ]

    responses = {
        0: {"intent": "greetings", "response": ['Hi Dear', 'Hi', 'Hello', 'Nice to see you', ]},
        1: {"intent": "studentid", "response": ['Welcome to Lambton {username}!']},
        11: {"intent": "grade", "response": ['Hi {username}, your grades are as follows\n {grades}']},
        12: {"intent": "fee", "response": ['Hi {username}, your total college_fee is {college_fee}']},
        13: {"intent": "date", "response": ['Hi {username}, your exam date is {exam_date}']},
        9: {"intent": "goodbye", "response": ['Goodbye', 'Byebye', 'Bye', 'Have a good day']},
        10: {"intent": "thankyou",
             "response": ['You\'re welcome.', 'No problem.', 'No worries.', ' My pleasure.', 'Glad to help.']}}

    with open('application-config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    df = pd.DataFrame(data, columns=["Text", "Intent"])
    lemmer = nltk.stem.WordNetLemmatizer()
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    x = df['Text']
    y = df['Intent']
    vectorizer = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    X = vectorizer.fit_transform(x)
    lr = LogisticRegression()
    lr.fit(X, y)
    X_test = ["flowers"]
    prediction = lr.predict(vectorizer.transform(X_test))
    lr.predict_proba(vectorizer.transform(X_test))
    main()
