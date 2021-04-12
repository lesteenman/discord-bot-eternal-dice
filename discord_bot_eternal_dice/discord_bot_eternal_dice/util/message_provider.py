from abc import ABC

from discord_bot_eternal_dice.model.dice_roll import DiceRoll


class MessageProvider(ABC):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> str:
        pass

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> str:
        pass


class MessageProviderImpl(MessageProvider):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> str:
        return f"{member_name} rolled a random number between {roll_min} and {roll_max}...\n\nIt's a *{number}*!"

    def roll_dice(self, member_name: str, expression: str, result: int) -> str:
        pass
