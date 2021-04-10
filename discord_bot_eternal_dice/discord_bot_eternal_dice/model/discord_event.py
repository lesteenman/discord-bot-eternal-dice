from enum import Enum
from typing import Dict

from discord_interactions import InteractionType

from discord_bot_eternal_dice.model.discord_command import DiscordCommand, command_from_data
from discord_bot_eternal_dice.model.discord_member import DiscordMember, member_from_data


class CommandType(Enum):
    PING = 1
    COMMAND = 2


class DiscordEvent:
    def __init__(self, command_type: CommandType, command: DiscordCommand = None, member: DiscordMember = None,
                 guild_id: int = None, channel_id: int = None):
        self.type = command_type
        self.command = command
        self.member = member
        self.guild_id = guild_id
        self.channel_id = channel_id


def from_event(event_source: Dict) -> DiscordEvent:
    if event_source['type'] == InteractionType.PING:
        return DiscordEvent(command_type=CommandType.PING)
    else:
        return DiscordEvent(
            command_type=CommandType.COMMAND,
            channel_id=int(event_source['channel_id']),
            guild_id=int(event_source['guild_id']),
            command=command_from_data(event_source['data']),
            member=member_from_data(event_source['member'])
        )
