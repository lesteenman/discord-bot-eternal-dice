import json
import typing
from typing import Dict

from discord_bot_eternal_dice import handler
from discord_bot_eternal_dice.model.discord_event import CommandType

DEFAULT_GUILD_ID = 10
DEFAULT_CHANNEL_ID = 300
DEFAULT_USER_ID = 400
DEFAULT_ROLE_ID = 500
DEFAULT_USER_NAME = "default-username"
DEFAULT_MEMBER_NICK = "default-nickname"


def create_context() -> Dict:
    return {}


def test_integration_roll_numbers():
    # Try to roll a few random numbers
    roll_random_number(-50, 200)
    roll_random_number(100, 200)
    roll_random_number(1, 20)
    roll_random_number(1, 5)

    # Try a few sets of dice
    roll_dice("1d20")
    roll_dice("d10")
    roll_dice("5d20+6d6+18-1d100")


def roll_random_number(min_roll: int, max_roll: int):
    response = handler.handle_lambda(
        make_discord_event(
            roll_type="number",
            options=[
                {
                    "name": "min",
                    "value": min_roll,
                },
                {
                    "name": "max",
                    "value": max_roll,
                },
            ],
        ),
        create_context()
    )

    assert response['statusCode'] == 200


def roll_dice(expression: str):
    response = handler.handle_lambda(
        make_discord_event(
            roll_type="dice",
            options=[
                {
                    "name": "expression",
                    "value": expression,
                },
            ],
        ),
        create_context()
    )

    assert response['statusCode'] == 200


def make_discord_event(roll_type: str, options: typing.List, guild_id: int = DEFAULT_GUILD_ID,
                       user_id: int = DEFAULT_USER_ID, channel_id: int = DEFAULT_CHANNEL_ID,
                       member_nickname: str = DEFAULT_MEMBER_NICK, user_name: str = DEFAULT_USER_NAME):

    event_body = _base_event_body(guild_id=guild_id, channel_id=channel_id, user_id=user_id,
                                  member_nickname=member_nickname, user_name=user_name)

    event_body['data'] = {
        "id": "2001",
        "name": "roll",
        "options": [
            {
                "name": roll_type,
                "options": options,
            }
        ]
    }

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


def _make_event(body: Dict) -> Dict:
    return {
        'body': json.dumps(body),
        'headers': {},
    }


def _create_member(user_id: int, member_nickname: str, user_name: str) -> Dict:
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
