import nltk
import sys

from bot.bot import Bot
from bot.skills.eliza import ElizaSkill
from bot.skills.math import MathSkill
from bot.skills.echo import EchoSkill


def main():
    bot = Bot(sys.argv[1], [
        MathSkill(),
        ElizaSkill('good_doctor.txt'),
        EchoSkill()
    ])
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()
