from bot import Bot
from EchoSkill import EchoSkill
from ElizaSkill import Template
import nltk

def main():
    bot = Bot('')
    template = Template(
        ['0', 'a', '2'],
        [[]]
    )
    match = template.match(['a', 'a', 'b'])[0]
    print(match.indexes)
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()
