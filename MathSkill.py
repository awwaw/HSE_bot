class MathSkill:
    def __init__(self):
        self.keywords = ['умножь', 'раздели', 'подели', 'сложи', 'плюс',
                         'минус', 'вычти', 'разность', 'частное', 'произведение', 'сумма',
                         'умножить', 'поделить', 'сложить', 'вычесть', 'делить', 'разделить'
                         'прибавь']

    def match(self, message: str) -> bool:
        for word in message.split():
            if word.lower() in self.keywords:
                return True
        return False

    def answer(self, message: str) -> str:
        nums = []
        operations = []
        for word in message.split():
            if word.isdigit():
                nums.append(int(word))
            elif word in self.keywords:
                if word.lower() in ['умножь', 'произведение', 'умножить']:
                    operations.append('*')
                elif word.lower() in ['раздели', 'подели', 'частное', 'поделить', 'делить', 'разделить']:
                    operations.append('/')
                elif word.lower() in ['сложи', 'плюс', 'сумма', 'сложить']:
                    operations.append('+')
                else:
                    operations.append('-')
        nums = nums[::-1]
        for ch in operations:
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
