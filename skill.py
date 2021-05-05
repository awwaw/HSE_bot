from telegram.ext import CallbackContext
from telegram import Update


class EchoSkill:
    def __init__(self, message: str, update: Update, context: CallbackContext):
        self.message = message
        self.keywords = []
        self.update = update
        self.context = context

    def match(self) -> bool:
        return bool(self.message)

    def answer(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id,
                                      text=self.update.message.text)