import json
import typing

from discord_bot_eternal_dice import handler
from discord_bot_eternal_dice.model.discord_response import ResponseType
from tests.integration.utilities import create_context, make_discord_event


def test_integration_roll_numbers():
    # No subcommand or options
    response = call_command(command="something_else")
    assert is_ephemeral_reply(response)

    # No options at all
    response = call_command(command="something_else", subcommand="banana")
    assert is_ephemeral_reply(response)

    # No subcommand or options
    response = call_command(command="something_else", options=[])
    assert is_ephemeral_reply(response)

    # An unknown command
    response = call_command(command="something_else", subcommand="banana", options=[])
    assert is_ephemeral_reply(response)

    # An unknown subcommand
    response = call_command(command="roll", subcommand="bananas", options=[])
    assert is_ephemeral_reply(response)

    # Missing parameters
    response = call_command(command="roll", subcommand="number", options=[{'name': 'min', 'value': 5}])
    assert is_ephemeral_reply(response)


def is_ephemeral_reply(response) -> bool:
    return response['type'] == ResponseType.REPLY.value and \
           is_ephemeral(response) and \
           type(response['data']['content']) == str and \
           len(response['data']['content']) > 0


def call_command(command: str, subcommand: str = None, options: typing.List[typing.Dict] = None) -> typing.Dict:
    response = handler.handle_lambda(
        make_discord_event(
            command=command,
            subcommand=subcommand,
            options=options,
        ),
        create_context()
    )

    assert response['statusCode'] == 200

    return json.loads(response['body'])


def is_ephemeral(response: typing.Dict) -> bool:
    return response['data']['flags'] & 64 == 64
