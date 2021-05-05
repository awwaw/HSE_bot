from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters


updater = Updater(token='1121091418:AAGRPeCAE_VR-fZhusOc3WWbwGPY8SRw0yw', use_context=True)
dispatcher = updater.dispatcher


import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='ABEBA')


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(message_handler)

updater.start_polling()
