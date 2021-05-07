from bot.bot import Skill


class EchoSkill(Skill):
    def __init__(self):
        self.keywords = []

    def match(self, message: str) -> bool:
        return bool(message)

    def answer(self, message: str):
        return message
