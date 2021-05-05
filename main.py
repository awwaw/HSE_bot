from bot import Bot
<<<<<<<<< Temporary merge branch 1
from EchoSkill import EchoSkill
=========
from skill import EchoSkill
from ELIZA import ELIZA
>>>>>>>>> Temporary merge branch 2


def main():
    bot = Bot('TOKEN')
    bot.run()


if __name__ == '__main__':
    main()
