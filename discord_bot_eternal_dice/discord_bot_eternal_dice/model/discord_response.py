import typing
from enum import Enum


class ResponseType(Enum):
    PONG = 1
    ACKNOWLEDGE = 2
    REPLY = 4


class DiscordEmbed:
    def __init__(self, title: str, description: str = "", footer: str = "", color: int = None):
        self.title = title
        self.description = description
        self.footer = footer
        self.color = color

    def to_dict(self) -> typing.Dict:
        converted = {
            'title': self.title,
            'description': self.description,
            'footer': {
                'text': self.footer,
            },
            'type': 'rich',
        }

        if self.color is not None:
            converted['color'] = self.color

        return converted


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

    # @classmethod
    # def acknowledge_with_source(cls):
    #     return DiscordResponse(
    #         response_type=ResponseType.ACKNOWLEDGE_WITH_SOURCE
    #     )
