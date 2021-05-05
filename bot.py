import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from telegram.ext import Updater, CallbackContext
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters
from EchoSkill import EchoSkill
from MathSkill import MathSkill


class Bot():
    def __init__(self, token: str):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_handler = MessageHandler(Filters.text & (~Filters.command), self.get_message)
        self.dispatcher.add_handler(self.message_handler)
        self.skills = [MathSkill(), EchoSkill()]

        self.message = self.get_message
        self.words = self.split_to_tokens()
        self.dict = {"were": "was", "'m": "i am", "'re": "you are"}

    def split_to_sent(self):
        tokenized_text = sent_tokenize(self.message)
        return tokenized_text

    def split_to_tokens(self):
        tokenized_text = self.split_to_sent()
        words = []
        for sent in tokenized_text:
            words.append(word_tokenize(sent))
        return words

    def process(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])):
                new_word = self.words[i][j].lower()
                if new_word in self.dict:
                    new_word = self.dict[new_word]
                self.words[i][j] = new_word

    def get_message(self, update: Update, context: CallbackContext):
        message = update.message.text
        for skill in self.skills:
            if skill.match(message):
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=skill.answer(message))
                break

    def run(self):
        self.updater.start_polling()

