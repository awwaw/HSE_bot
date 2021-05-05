from telegram.ext import CallbackContext
from telegram import Update


class EchoSkill:
    def __init__(self):
        self.keywords = []

    def match(self, message: str) -> bool:
        return bool(message)

    def answer(self, message: str):
        return message
