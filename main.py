from bot import Bot
from skill import EchoSkill
from ELIZA import ELIZA


def main():
    bot = Bot('TOKEN')
    bot.run()


if __name__ == '__main__':
    main()
