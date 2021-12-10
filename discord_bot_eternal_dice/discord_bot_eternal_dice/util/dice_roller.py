import random
import re
from abc import ABC

from discord_bot_eternal_dice.model.dice_roll import DiceRoll, DiceRollPartial, StaticPartial

PART_MATCHER = re.compile("([+-]?([0-9]+)?d?([0-9]+)?)")
DICE_MATCHER = re.compile("([+-])?([0-9]+)?d([0-9]+)")
EXTRA_MATCHER = re.compile("([+-])?([0-9]+)")


class DiceRoller(ABC):
    def roll(self, expression: str) -> DiceRoll:
        raise NotImplementedError()


class DiceRollerImpl(DiceRoller):
    def roll(self, expression: str) -> DiceRoll:
        dice_roll = DiceRoll(expression)

        for part_match in PART_MATCHER.findall(expression):
            part = part_match[0]
            if self.is_dice(part):
                self.match_dice(dice_roll, part)
            else:
                self.match_extra(dice_roll, part)

        self.perform_roll(dice_roll)

        return dice_roll

    def perform_roll(self, dice_roll):
        result = 0

        for partial in dice_roll.parts:
            if type(partial) is StaticPartial:
                result += partial.value

            if type(partial) is DiceRollPartial:
                for _ in range(0, partial.number):
                    roll = random.randint(1, partial.dice_type)
                    partial.results.append(roll)

                    if partial.is_negative:
                        result -= roll
                    else:
                        result += roll

        dice_roll.result = result

    def is_dice(self, expression):
        return DICE_MATCHER.match(expression) is not None

    def match_dice(self, dice_roll, expression):
        match = DICE_MATCHER.match(expression)
        if match is not None:
            is_negative = match.group(1) == "-"

            num_dice = match.group(2)
            if num_dice is None:
                num_dice = 1
            else:
                num_dice = int(num_dice)

            type_dice = int(match.group(3))

            if num_dice != 0:
                dice_roll.add(DiceRollPartial(
                    expression=expression,
                    is_negative=is_negative,
                    number=num_dice,
                    dice_type=type_dice,
                ))

    def match_extra(self, dice_roll, expression):
        match = EXTRA_MATCHER.match(expression)
        if match is not None:
            value = int(match.group(2))

            if match.group(1) == "-":
                value = -value

            dice_roll.add(StaticPartial(expression=expression, value=value))
