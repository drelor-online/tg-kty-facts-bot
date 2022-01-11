__version__ = "1.0.0"
import random
from uuid import uuid4

from decouple import config
from logzero import logger as log
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode, \
    ReplyKeyboardRemove
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from util import levenshteinDistance as distance


class Facts(object):
    def __init__(self):
        self.facts = []
        self.load_facts()

    def load_facts(self):
        with open("facts.txt", mode="r") as f:
            fact_lines = f.readlines()
        for fact in fact_lines:
            self.facts += [fact]

    def get_facts(self):
        return self.facts


all_facts = Facts()


def error(bot, update, error):
    log.error('Update "%s" caused error "%s"' % (update, error))

def get_random_fact():
    return random.choice(all_facts.get_facts())

def send_fact(bot, update):
    chat_id = update.message.chat_id
    fact = get_random_fact()
    log.info("Sending fact to " + str(chat_id) + ": " + fact)
    bot.sendMessage(chat_id, fact)


def main():
    bot_token = config("BOT_TOKEN")
    updater = Updater(bot_token)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("ktyfacts", send_fact))

    updater.start_polling()

    log.info("Listening...")

    updater.idle()


if __name__ == "__main__":
    main()
