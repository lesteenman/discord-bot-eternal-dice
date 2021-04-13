import json
import typing

from discord_bot_eternal_dice.model.discord_event import CommandType

DEFAULT_GUILD_ID = 10
DEFAULT_CHANNEL_ID = 300
DEFAULT_USER_ID = 400
DEFAULT_ROLE_ID = 500
DEFAULT_USER_NAME = "default-username"
DEFAULT_MEMBER_NICK = "default-nickname"


def make_discord_event(command: str, subcommand: str, options: typing.List, guild_id: int = DEFAULT_GUILD_ID,
                       user_id: int = DEFAULT_USER_ID, channel_id: int = DEFAULT_CHANNEL_ID,
                       member_nickname: str = DEFAULT_MEMBER_NICK, user_name: str = DEFAULT_USER_NAME):

    event_body = _base_event_body(guild_id=guild_id, channel_id=channel_id, user_id=user_id,
                                  member_nickname=member_nickname, user_name=user_name)

    event_body['data'] = {
        "id": "2001",
        "name": command,
    }

    if subcommand and options:
        event_body['data']['options'] = [
            {
                "name": subcommand,
                "options": options,
            }
        ]
    elif subcommand:
        event_body['data']['options'] = [
            {
                'name': subcommand
            }
        ]
    elif options:
        event_body['data']['options'] = options

    return _make_event(event_body)


def _base_event_body(guild_id: int, channel_id: int, user_id: int, member_nickname: str, user_name: str):
    return {
        "channel_id": channel_id,
        "guild_id": guild_id,
        "data": None,
        "id": "9991",
        "member": _create_member(
            user_id=user_id,
            member_nickname=member_nickname,
            user_name=user_name,
        ),
        "token": "whfjwhfukwynexfl823yflwf9wauf928fh82e",
        "type": CommandType.COMMAND.value,
        "version": 1
    }


def _make_event(body: typing.Dict) -> typing.Dict:
    return {
        'body': json.dumps(body),
        'headers': {},
    }


def _create_member(user_id: int, member_nickname: str, user_name: str) -> typing.Dict:
    return {
        "deaf": False,
        "is_pending": False,
        "joined_at": "2021-01-16T20:21:19.053000+00:00",
        "mute": False,
        "nick": member_nickname,
        "pending": False,
        "permissions": 0,
        "premium_since": None,
        "roles": [],
        "user": {
            "avatar": "abcdefghijklmop",
            "discriminator": "5",
            "id": user_id,
            "public_flags": 0,
            "username": user_name
        }
    }


def create_context() -> typing.Dict:
    return {}
