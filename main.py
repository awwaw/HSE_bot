import nltk
import sys

from bot.bot import Bot
from bot.skills.eliza import ElizaSkill
from bot.skills.math import MathSkill
from bot.skills.echo import EchoSkill
from bot.skills.pushkin import PushkinSkill
from bot.skills.dialogue import DialogueSkill

from datetime import datetime as dt

def main():
    bot = Bot(sys.argv[1], [
        MathSkill(),
        PushkinSkill('static/documents/save_state.tmp'),
        DialogueSkill(),
        ElizaSkill('good_doctor.txt'),
        EchoSkill()
    ])
    bot.run()


if __name__ == '__main__':
    # nltk.download('punkt')
    rf = Classifier(max_depth=3)
    rf.prepare_data('static/documents/unique_dialogues.txt')

    start = dt.now()
    rf.test()
    end = dt.now()
    print(end - start)
    main()
