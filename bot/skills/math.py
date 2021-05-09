from bot.bot import Skill


class MathSkill(Skill):
    def __init__(self):
        self.keywords = ['умножь', 'произведение', 'умножить', 'домножь', 'домножить',
                         'раздели', 'подели', 'частное', 'поделить', 'делить', 'разделить',
                         'сложи', 'плюс', 'сумма', 'сложить', 'прибавь', 'прибавить', 'суммировать',
                         'минус', 'вычти', 'разность', 'вычесть', 'отнять', 'отними']

    def match(self, message: str) -> bool:
        for word in message.split():
            if word.lower() in self.keywords:
                return True
        return False

    def answer(self, message: str) -> str:
        nums = []
        operations = []
        for word in message.lower().split():
            if word.isdigit():
                nums.append(int(word))
            elif word in self.keywords:
                if word in ['умножь', 'произведение', 'умножить', 'домножь', 'домножить']:
                    operations.append('*')
                elif word in ['раздели', 'подели', 'частное', 'поделить', 'делить', 'разделить']:
                    operations.append('/')
                elif word in ['сложи', 'плюс', 'сумма', 'сложить', 'прибавь', 'прибавить', 'суммировать']:
                    operations.append('+')
                elif word in ['минус', 'вычти', 'разность', 'вычесть', 'отнять', 'отними']:
                    operations.append('-')
                else:
                    pass
        nums = nums[::-1]

        if len(nums) < 2:
            return 'Недостаточно информации'

        for ch in operations[:len(nums) - 1]:
            a = nums[-1]
            nums.pop(-1)
            b = nums[-1]
            nums.pop(-1)
            if ch == '+':
                nums.append(a + b)
            elif ch == '-':
                nums.append(a - b)
            elif ch == '/':
                nums.append(a / b)
            else:
                nums.append(a * b)
        return str(nums[-1])
