from bot import Bot
import nltk
from EchoSkill import EchoSkill


def main():
    nltk.download('punkt')
    bot = Bot("1665573427:AAEuFh15FLJfoAqGrAXuE6xY30wmpcGu3qY")
    bot.run()


if __name__ == '__main__':
    main()