from abc import ABC

from discord_bot_eternal_dice.model.dice_roll import DiceRoll, StaticPartial, DiceRollPartial
from discord_bot_eternal_dice.util.dice_roller import DiceRollerImpl


class MessageProvider(ABC):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> str:
        pass

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> str:
        pass


class MessageProviderImpl(MessageProvider):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> str:
        return f"{member_name} rolled a random number between {roll_min} and {roll_max}...\n\nIt's a *{number}*!"

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> str:
        rolls = []
        for part in dice_roll.parts:
            if type(part) is StaticPartial:
                if part.value >= 0:
                    rolls.append("+")
                rolls.append(str(part.value))
            elif type(part) is DiceRollPartial:
                for result in part.results:
                    if result >= 0:
                        rolls.append("+")
                    rolls.append(str(result))

        roll_expression = "".join(rolls)
        if roll_expression[0] == "+":
            roll_expression = roll_expression[1:]

        return f"{member_name} rolled _{dice_roll.expression}_ for a total of *{dice_roll.result}* ({roll_expression})"


if __name__ == '__main__':
    provider = MessageProviderImpl()
    dice_roller = DiceRollerImpl()

    print(provider.roll_dice(
        "Erik",
        dice_roller.roll("1d100+3"),
    ))
