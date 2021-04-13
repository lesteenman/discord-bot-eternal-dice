from enum import Enum


class ResponseType(Enum):
    PONG = 1
    ACKNOWLEDGE = 2
    REPLY = 4


class DiscordResponse(object):
    def __init__(self, response_type: ResponseType, content: str = None, allow_role_mentions: bool = False,
                 allow_user_mentions: bool = False):
        self.response_type = response_type

        if content is None:
            self.data = None
        else:
            self.data = {
                'content': content,
            }

        self.allowed_mention_types = []
        if allow_user_mentions:
            self.allowed_mention_types.append('users')
        if allow_role_mentions:
            self.allowed_mention_types.append('roles')

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
            content=content,
        )

    # @classmethod
    # def acknowledge_with_source(cls):
    #     return DiscordResponse(
    #         response_type=ResponseType.ACKNOWLEDGE_WITH_SOURCE
    #     )
