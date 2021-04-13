class StaticPartial:
    def __init__(self, expression: str, value: int):
        self.expression = expression
        self.value = value


class DiceRollPartial:
    def __init__(self, expression: str, is_negative: bool, number: int, dice_type: int):
        self.expression = expression
        self.is_negative = is_negative
        self.number = number
        self.dice_type = dice_type
        self.results = []


class DiceRoll:
    def __init__(self, expression):
        self.expression = expression
        self.parts = []
        self.result = None

    def add(self, partial: DiceRollPartial):
        self.parts.append(partial)
