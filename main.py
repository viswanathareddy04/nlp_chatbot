import logging
import sys

import pandas as pd

from bot_responses import BotResponses
from lambton_AIML_Bot import LambtonBot
from nltk_process import NLTK_Process
from telegram_bot import TelegramConnect

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    botResponse = BotResponses()
    lambtonBot = LambtonBot()
    config = lambtonBot.readConfig('application-config.yaml')
    df = pd.DataFrame(botResponse.data, columns=["Text", "Intent"])
    nltkprocess = NLTK_Process
    nltkprocess.performLogisticRegression(df)
    telegramConnect = TelegramConnect(config['telegram']['token'])
    telegramConnect.telegramPolling()
