# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:10:28 2022

@author: Group 4
"""
import logging
import sys

from telegram.ext import Updater, MessageHandler, Filters

from lambton_AIML_Bot import LambtonBot

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class TelegramConnect:

    def __init__(self, token):
        self.token = token

    def telegramPolling(self):
        try:
            lambtonBot = LambtonBot
            updater = Updater(self.token, use_context=True)
            updater.dispatcher.add_handler(MessageHandler(Filters.text, lambtonBot().bot_initialize))
            updater.start_polling()
            updater.idle()
        except:
            print("Error connecting telegram bot ")
