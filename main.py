from bot import Bot
import nltk
from EchoSkill import EchoSkill
import nltk


def main():
    bot = Bot('')
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()
