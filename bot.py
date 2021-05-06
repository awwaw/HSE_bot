from nltk.tokenize import sent_tokenize, word_tokenize
from telegram.ext import Updater, CallbackContext
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters
from EchoSkill import EchoSkill
from MathSkill import MathSkill


class Bot:
    def __init__(self, token: str):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_handler = MessageHandler(Filters.text & (~Filters.command), self.get_message)
        self.dispatcher.add_handler(self.message_handler)
        self.skills = [MathSkill(), EchoSkill()]
        self.dict = {"were": "was", "i'm": "i am", "you're": "you are"}

    def split_to_sent(self, sentence: str):
        tokenized_text = sent_tokenize(sentence)
        return tokenized_text

    def split_to_tokens(self, sentences: str):
        punctuations = '''!()-[]{};:\,<>./?@#$%^&*_~'''
        tokenized_text = self.split_to_sent(sentences)
        words = []
        for sent in tokenized_text:
            no_punct_sent = ""
            for char in sent:
                if char not in punctuations:
                    no_punct_sent = no_punct_sent + char
            words.append(no_punct_sent.split())
        return words

    def preprocess(self, sentences: str):
        words = self.split_to_tokens(sentences)
        for i in range(len(words)):
            for j in range(len(words[i])):
                new_word = words[i][j].lower()
                if new_word in self.dict:
                    new_word = self.dict[new_word]
                words[i][j] = new_word
        return words

    def get_message(self, update: Update, context: CallbackContext):
        message = update.message.text

        answer = str(self.preprocess(message))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=answer)
        # for skill in self.skills:
        #     if skill.match(message):
        #         context.bot.send_message(chat_id=update.effective_chat.id,
        #                                  text=skill.answer(message))
        #         break

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
