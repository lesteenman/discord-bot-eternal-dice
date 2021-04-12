from discord_bot_eternal_dice.model import discord_event


def test_from_ping_event():
    # Given
    event_body = {
        "id": "5002",
        "token": "whfjwhfukwynexfl823yflwf9wauf928fh82d",
        "type": 1,
        "version": 1
    }

    # When
    event = discord_event.from_event(event_body)

    # Then
    assert event.type == discord_event.CommandType.PING
    assert event.command is None


def test_member_from_event():
    # Given
    event_body = {
        "channel_id": "1001",
        "data": {
            "id": "2001",
            "name": "roll",
            "options": [
                {
                    "name": "number",
                    "options": [
                        {
                            "name": "min",
                            "value": 10,
                        },
                        {
                            "name": "max",
                            "value": 30,
                        },
                    ]
                }
            ]
        },
        "guild_id": "4001",
        "id": "5001",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2021-01-16T20:21:19.053000+00:00",
            "mute": False,
            "nick": "User-Nickname",
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": [
                "9999",
            ],
            "user": {
                "avatar": "abcdefghijklmop",
                "discriminator": "5",
                "id": "9001",
                "public_flags": 0,
                "username": "User-Name"
            }
        },
        "token": "whfjwhfukwynexfl823yflwf9wauf928fh82e",
        "type": 2,
        "version": 1
    }

    # When
    event = discord_event.from_event(event_body)

    # Then
    assert event.member.username == "User-Name"
    assert event.member.nickname == "User-Nickname"
    assert event.member.user_id == 9001


def test_from_roll_number_event():
    # Given
    event_body = {
        "channel_id": "1001",
        "data": {
            "id": "2001",
            "name": "roll",
            "options": [
                {
                    "name": "number",
                    "options": [
                        {
                            "name": "min",
                            "value": 10,
                        },
                        {
                            "name": "max",
                            "value": 30,
                        },
                    ]
                }
            ]
        },
        "guild_id": "4001",
        "id": "5001",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2021-01-16T20:21:19.053000+00:00",
            "mute": False,
            "nick": None,
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": [],
            "user": {
                "avatar": "abcdefghijklmop",
                "discriminator": "5",
                "id": "9001",
                "public_flags": 0,
                "username": "User-Name"
            }
        },
        "token": "whfjwhfukwynexfl823yflwf9wauf928fh82e",
        "type": 2,
        "version": 1
    }

    # When
    event = discord_event.from_event(event_body)

    # Then
    assert event.type == discord_event.CommandType.COMMAND
    assert event.channel_id == 1001
    assert event.guild_id == 4001

    command = event.command
    assert command.command_id == 2001
    assert command.command_name == "roll"
    assert command.subcommand_name == "number"
    assert command.options['min'] == 10
    assert command.options['max'] == 30


def test_from_roll_dice_event():
    # Given
    event_body = {
        "channel_id": "1001",
        "data": {
            "id": "2001",
            "name": "roll",
            "options": [
                {
                    "name": "dice",
                    "options": [
                        {
                            "name": "expression",
                            "value": "3d6+8d8",
                        },
                    ]
                }
            ]
        },
        "guild_id": "4001",
        "id": "5001",
        "member": {
            "deaf": False,
            "is_pending": False,
            "joined_at": "2021-01-16T20:21:19.053000+00:00",
            "mute": False,
            "nick": None,
            "pending": False,
            "permissions": "2147483647",
            "premium_since": None,
            "roles": [],
            "user": {
                "avatar": "abcdefghijklmop",
                "discriminator": "5",
                "id": "9001",
                "public_flags": 0,
                "username": "User-Name"
            }
        },
        "token": "whfjwhfukwynexfl823yflwf9wauf928fh82e",
        "type": 2,
        "version": 1
    }

    # When
    event = discord_event.from_event(event_body)

    # Then
    assert event.type == discord_event.CommandType.COMMAND
    assert event.channel_id == 1001
    assert event.guild_id == 4001

    command = event.command
    assert command.command_id == 2001
    assert command.command_name == "roll"
    assert command.subcommand_name == "dice"
    assert command.options['expression'] == "3d6+8d8"
