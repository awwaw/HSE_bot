from typing import List

from telegram.ext import Updater, CallbackContext
from telegram import Update
from telegram.ext import MessageHandler, Filters


class Skill:
    def match(self, message: str) -> bool:
        raise NotImplemented

    def answer(self, message: str) -> str:
        raise NotImplemented


class Bot:
    def __init__(self, token: str, skills: List[Skill]):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_handler = MessageHandler(Filters.text & (~Filters.command), self.get_message)
        self.dispatcher.add_handler(self.message_handler)
        self.skills = skills

    def get_message(self, update: Update, context: CallbackContext):
        message = update.message.text
        for skill in self.skills:
            if skill.match(message):
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=skill.answer(message))
                break

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
