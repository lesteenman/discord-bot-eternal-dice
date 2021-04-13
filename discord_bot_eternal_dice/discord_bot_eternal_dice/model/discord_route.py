import typing

from discord_bot_eternal_dice.model.discord_command import DiscordCommand
from discord_bot_eternal_dice.model.discord_event import CommandType, DiscordEvent


class DiscordRoute:
    def __init__(self, handler, command_type: CommandType, command: str, subcommand: str = None,
                 options: typing.Dict = None):
        self.handler = handler
        self.command_type = command_type
        self.subcommand = subcommand
        self.command = command
        self.options = options

    def matches(self, event: DiscordEvent) -> bool:
        if event.command.command_name != self.command:
            return False

        if event.command.subcommand_name is not None and event.command.subcommand_name != self.subcommand:
            return False

        return True

    def validate(self, command: DiscordCommand) -> bool:
        unconsumed_options = list(command.options.keys())

        for option, option_type in self.options.items():
            if option not in command.options:
                return False

            if type(command.options[option]) is not option_type:
                return False

            unconsumed_options.remove(option)

        if len(unconsumed_options) > 0:
            return False

        return True
