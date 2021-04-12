class StaticPartial:
    def __init__(self, value: int):
        self.value = value


class DiceRollPartial:
    def __init__(self, is_negative: bool, number: int, dice_type: int):
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
