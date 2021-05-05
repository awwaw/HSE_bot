class EchoSkill():
    def __init__(self, message, update, context):
        self.message = message
        self.keywords = []
        self.update = update
        self.context = context

    def match(self, message):
        return True

    def answer(self):
        self.context.bot.send_message(chat_id=update.effective_chat.id,
                                      text=update.message.text)