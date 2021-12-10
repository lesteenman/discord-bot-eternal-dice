from abc import ABC

from discord_bot_eternal_dice.api.router import DiscordRoute
from discord_bot_eternal_dice.model.dice_roll import DiceRoll, StaticPartial, DiceRollPartial
from discord_bot_eternal_dice.model.discord_command import DiscordCommand
from discord_bot_eternal_dice.model.discord_response import DiscordEmbed

COLOR_ETERNAL_BLUE = 0x9af5f4


class MessageProvider(ABC):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, result: int) -> DiscordEmbed:
        raise NotImplementedError()

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> DiscordEmbed:
        raise NotImplementedError()

    def unknown_command(self, command: DiscordCommand) -> str:
        raise NotImplementedError()

    def command_usage(self, route: DiscordRoute) -> str:
        raise NotImplementedError()


def format_option(option, option_type):
    if option_type is int:
        return f"{option}:<number>"

    if option_type is str:
        return f"{option}:<text>"

    raise ValueError(f"unhandled option_type: {option_type}")


class MessageProviderImpl(MessageProvider):
    def roll_number(self, member_name: str, roll_min: int, roll_max: int, result: int) -> DiscordEmbed:
        return DiscordEmbed(
            title=f"{member_name} rolled a number!",
            description=f"The result: **{result}**",
            footer=f"The number rolled was between {roll_min} and {roll_max}.",
            color=COLOR_ETERNAL_BLUE,
        )

    def roll_dice(self, member_name: str, dice_roll: DiceRoll) -> DiscordEmbed:
        rolls = []
        for part in dice_roll.parts:
            if type(part) is StaticPartial:
                rolls.append(part.expression)
            elif type(part) is DiceRollPartial:
                sub_rolls = []
                for result in part.results:
                    if result >= 0:
                        sub_rolls.append("+")
                    sub_rolls.append(str(result))
                rolls.append(part.expression)

                sub = "".join(sub_rolls)
                if sub[0] == "+":
                    sub = sub[1:]

                rolls.append(f"({sub})")

        roll_expression = "".join(rolls)
        if roll_expression[0] == "+":
            roll_expression = roll_expression[1:]

        if len(dice_roll.parts) == 1:
            return DiscordEmbed(
                title=f"{member_name} rolled a die!",
                description=f"The result: **{dice_roll.result}**",
                footer=f"The dice rolled: {roll_expression}",
                color=COLOR_ETERNAL_BLUE,
            )
        else:
            return DiscordEmbed(
                title=f"{member_name} rolled a bunch of dice!",
                description=f"The grand total: **{dice_roll.result}**",
                footer=f"The dice rolled: {roll_expression}",
                color=COLOR_ETERNAL_BLUE,
            )

    def unknown_command(self, command: DiscordCommand) -> str:
        return f"Unknown command: '/{command.command_name} {command.subcommand_name}'."

    def command_usage(self, route: DiscordRoute) -> str:
        options = " ".join([format_option(option, option_type) for option, option_type in route.options.items()])
        return f"Usage: '/{route.command} {route.subcommand} {options}'"
