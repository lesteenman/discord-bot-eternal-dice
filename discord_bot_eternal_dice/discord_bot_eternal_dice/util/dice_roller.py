from abc import ABC

from discord_bot_eternal_dice.model.dice_roll import DiceRoll


class DiceRoller(ABC):
    def roll(self, expression: str) -> DiceRoll:
        pass


class DiceRollerImpl(DiceRoller):
    pass
