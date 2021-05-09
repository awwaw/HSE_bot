import nltk
import sys

from bot.bot import Bot
from bot.skills.eliza import ElizaSkill
from bot.skills.math import MathSkill
from bot.skills.echo import EchoSkill
from bot.skills.pushkin import PushkinSkill
from bot.skills.dialogue import DialogueSkill


def main():
    bot = Bot(sys.argv[1], [
        MathSkill(),
        DialogueSkill(),
        PushkinSkill('static/documents/save_state.tmp'),
        ElizaSkill('good_doctor.txt'),
        EchoSkill()
    ])
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()