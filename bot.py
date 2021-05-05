from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters


class Bot():
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_handler = MessageHandler(Filters.text & (~Filters.command), self.get_message())
        self.dispatcher.add_handler(self.message_handler)

    def get_message(self, update, context):
        return update.message.text



    def run(self):
        self.updater.start_polling()