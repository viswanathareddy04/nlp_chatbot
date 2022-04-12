# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:51:15 2022

@author: Group 4
"""

import logging
import random
import sys
from datetime import datetime as date

import yaml

from bot_responses import BotResponses
from nltk_process import NLTK_Process

student_id = ''
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class LambtonBot:

    def __init__(self):
        self.botResponses = BotResponses()

    def bot_initialize(self, update, context):
        logger.info("bot initialization in process")
        botResponses = BotResponses()
        nltkprocess = NLTK_Process
        global student_id
        student_info = botResponses.student_information.get(student_id) or {}
        user_msg = update.message.text
        print(user_msg)
        flag = True
        while flag:
            user_response = user_msg
            user_intent = nltkprocess.intent(user_response)
            if user_intent != 'goodbye':
                if user_response.lower().startswith('c0'):
                    student_id = user_response or 'C01'
                    if botResponses.student_information.get(student_id, {}).get('name') == None:
                        return update.message.reply_text(
                            "Sorry I wasn't be able to find you in the database, make sure you have entered correct ID")
                    resp = str(random.choice(botResponses.responses[1]['response'])).format(
                        username=botResponses.student_information.get(student_id, {}).get('name'))
                    what_we_do = """Hi! Here is what I can do!!! \n1. I can give you your Grades\n2. College Fee\n3. Exam Dates.\n4 Today class details \n\n5. or Type goodbye to Exit."""
                    update.message.reply_text(resp + '\n' + what_we_do)
                    return

                if user_response == '/start' or not student_id:
                    resp = str(random.choice(
                        botResponses.responses[0][
                            'response'])) + ", Before we start, can I get your student ID please? ex: C0X"
                    update.message.reply_text(resp)
                    return

                if user_intent == "grade":
                    resp = str(random.choice(botResponses.responses[11]['response'])).format(
                        username=student_info.get('name'),
                        grades=student_info.get('grades'))
                    update.message.reply_text(resp)
                    return

                if user_intent == "fee":
                    resp = str(random.choice(botResponses.responses[12]['response'])).format(
                        username=student_info.get('name'),
                        college_fee=student_info.get('fee'))
                    update.message.reply_text(resp)
                    return

                if user_intent == "date":
                    resp = str(random.choice(botResponses.responses[13]['response'])).format(
                        username=student_info.get('name'),
                        exam_date=student_info.get('exam'))
                    update.message.reply_text(resp)
                    return

                if user_intent == "time":
                    today = date.today().strftime("%A")
                    if today == "Saturday" or today == "Sunday":
                        class_subj = "You do not have any classes today"
                    else:
                        class_subj = "You have " + botResponses.subjects.get(
                            today) + " please use this URL to join class https://moodle.cestarcollege.com/moodle/mod/url/view.php?id=1003405"

                    resp = str(random.choice(botResponses.responses[14]['response'])).format(
                        username=student_info.get('name'),
                        class_subj=class_subj)
                    update.message.reply_text(resp)
                    return

                if user_intent == 'thankyou':
                    resp = random.choice(botResponses.responses[10]['response'])
                    update.message.reply_text(resp)
                    return

                resp = "Ummm! Please rephrase your sentence. I am not that smart."
                update.message.reply_text(resp)
                return
            else:
                flag = False
                resp = random.choice(botResponses.responses[9]['response'])
                update.message.reply_text(resp)
                return

    def readConfig(self, config_file):
        logger.info("Read Config file")
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except:
            print("Config File not found")
