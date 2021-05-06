from bot import Bot
from EchoSkill import EchoSkill
import nltk

def main():
    bot = Bot('1751454916:AAEGnqf0okA7PX5N0oeJU0MzdliJrMgtcpo')
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()
