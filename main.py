from bot import Bot
from EchoSkill import EchoSkill
from ElizaSkill import Template
from Match import Match
import nltk

def main():
    bot = Bot('1121091418:AAGRPeCAE_VR-fZhusOc3WWbwGPY8SRw0yw')
    template = Template(
        ['0', 'niggers'],
        [[]]
    )
    match = template.match(['a', 'a', 'b'], ['0', 'a', '2'], 0, 0, [])[0]
    print(match.indexes)
    bot.run()


if __name__ == '__main__':
    nltk.download('punkt')
    main()
