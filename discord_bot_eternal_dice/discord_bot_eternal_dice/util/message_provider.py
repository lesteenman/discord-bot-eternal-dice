from abc import ABC

from discord_bot_eternal_dice.model.dice_roll import DiceRoll, StaticPartial, DiceRollPartial
from discord_bot_eternal_dice.model.discord_response import DiscordEmbed

COLOR_ETERNAL_BLUE = 0x9af5f4


class MessageProvider(ABC):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> DiscordEmbed:
        pass

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> DiscordEmbed:
        pass


class MessageProviderImpl(MessageProvider):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, number: int) -> DiscordEmbed:
        return DiscordEmbed(
            title=f"{member_name} rolled a number!",
            description=f"The result: **{number}**",
            footer=f"The number rolled was between {roll_min} and {roll_max}.",
            color=COLOR_ETERNAL_BLUE,
        )

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> DiscordEmbed:
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

        if len(dice_roll.parts) > 1:
            return DiscordEmbed(
                title=f"{member_name} rolled a dice!",
                description=f"The result: **{dice_roll.result}**",
                footer=f"The dice rolled: {roll_expression}",
                color=COLOR_ETERNAL_BLUE,
            )
        else:
            return DiscordEmbed(
                title=f"{member_name} rolled a bunch of dice!",
                description=f"The grand total: **{result}**",
                footer=f"The dice rolled: {roll_expression}",
                color=COLOR_ETERNAL_BLUE,
            )
