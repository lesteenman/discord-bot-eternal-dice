import typing
from enum import Enum

from discord_bot_eternal_dice.model.discord_embed import DiscordEmbed


class ResponseType(Enum):
    PONG = 1
    ACKNOWLEDGE = 2
    REPLY = 4


class DiscordResponse:
    def __init__(self, response_type: ResponseType, data: typing.Dict = None):
        self.response_type = response_type
        self.data = data

    def json(self):
        if self.data is not None:
            return {
                'type': self.response_type.value,
                'data': self.data,
            }
        else:
            return {
                'type': self.response_type.value,
            }

    @classmethod
    def pong(cls):
        return DiscordResponse(
            response_type=ResponseType.PONG
        )

    @classmethod
    def acknowledge(cls):
        return DiscordResponse(
            response_type=ResponseType.ACKNOWLEDGE
        )

    @classmethod
    def reply(cls, content: str):
        return DiscordResponse(
            response_type=ResponseType.REPLY,
            data={
                'content': content,
            },
        )

    @classmethod
    def embed_reply(cls, embed: DiscordEmbed):
        return DiscordResponse(
            response_type=ResponseType.REPLY,
            data={
                'embeds': [embed.to_dict()],
            },
        )

    @classmethod
    def ephemeral_reply(cls, message):
        return DiscordResponse(
            response_type=ResponseType.REPLY,
            data={
                'content': message,
                'flags': 64,
            }
        )
