import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


class Bot():
    def __init__(self, message):
        self.message = message
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


nltk.download('punkt')
bot = Bot("Hello! I'm Azalia, and you're our bot. You WERE created by US. 1234")
bot.process()
print(bot.words)