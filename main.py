import nltk
import sys

from bot.bot import Bot
from bot.skills.eliza import ElizaSkill
from bot.skills.math import MathSkill
from bot.skills.echo import EchoSkill

from RF import Classifier


def main():
    bot = Bot(sys.argv[1], [
        MathSkill(),
        ElizaSkill('doctor.txt'),
        EchoSkill()
    ])
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    rf = Classifier()
    rf.prepare_data('static/documents/unique_dialogues.txt')
    # print(rf.text)
    main()
