# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:51:15 2022

@author: Group 4
"""

import logging
import random
import string
import sys
from datetime import datetime as date
import nltk
import pandas as pd
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from telegram.ext import Updater, MessageHandler, Filters

student_id = ''
today = date.today().strftime("%A")
print(today)

student_information = {
    "C01": {
        "name": "John",
        "exam": "April 14, 2022",
        "grades": "CBD: 89%\nALML:95%",
        "fee": "$200",
    },
    "C02": {
        "name": "Dan",
        "exam": "April 14, 2022",
        "grades": "CBD: 90%\nALML:95%",
        "fee": "$100",
    },
    "C03": {
        "name": "Michelle",
        "exam": "April 14, 2022",
        "grades": "CBD: 79%\nALML:95%",
        "fee": "$150",
    },
    "C04": {
        "name": "Rosi",
        "exam": "April 14, 2022",
        "grades": "CBD: 84%\nALML:95%",
        "fee": "$230",
       
    }
}

subjects =   {"Monday": "Into to AI at 1:00 PM to 4.30 PM", "Tuesday": "CBD at 12:30 PM to 4.30 PM" , "Wednesday": "Python at 12:30 PM to 4.30 PM", "Thursday": "DS at 08:00 AM to 12.30 PM","Friday":"Communication at 11.30 AM to 4:00 PM", "Saturday": "No classes today", "Sunday": "No classes today"}



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
                what_we_do = """Hi! Here is what I can do!!! \n1. I can give you your Grades\n2. College Fee\n3. Exam Dates.\n4 Today class details \n\n5. or Type goodbye to Exit."""
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
            
            if user_intent == "time":
                resp = str(random.choice(responses[14]['response'])).format(username=student_info.get('name'),
                                                                            class_subj=subjects.get(today))
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
        ["Goodbye", 9], ["Byebye", 9], ["Bye", 9],
        ["Thanku", 10], ["Thank You", 10], ["Thanks", 10], ["Thanks a lot", 10], ["Thank you very much", 10],
        ["Thank you so much", 10],
        ["grade", 11], ['grades', 11], ['marks', 11],
        ["fee", 12], ['college fee', 12], ['semester fee', 12],
        ["subject time", 14], ['class time', 14], ['today class time', 14], ['today subject class time', 14],
        ["final exam date", 13], ['exam date', 13], ['semester date', 13],
    ]

    responses = {
        0: {"intent": "greetings", "response": ['Hi Dear', 'Hi', 'Hello', 'Nice to see you', ]},
        1: {"intent": "studentid", "response": ['Welcome to Lambton {username}!']},
        11: {"intent": "grade", "response": ['Hi {username}, your grades are as follows\n {grades}']},
        12: {"intent": "fee", "response": ['Hi {username}, your total college_fee is {college_fee}. Please visit this URL to pay the fee https://www.lambtoncollege.ca/custom/LambtonApps/Payments/SecurePay.aspx']},
        13: {"intent": "date", "response": ['Hi {username}, your exam date is {exam_date}']},
        14: {"intent": "time", "response": ['Hi {username}, you have {class_subj} . please use this URL to join class https://moodle.cestarcollege.com/moodle/mod/url/view.php?id=1003405']},
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
