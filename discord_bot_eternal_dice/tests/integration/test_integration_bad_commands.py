import json
import typing

from discord_bot_eternal_dice import handler
from discord_bot_eternal_dice.model.discord_response import ResponseType
from tests.integration.utilities import create_context, make_discord_event


def test_integration_roll_numbers():
    # An unknown command will reply with an ephemeral channel response
    response = make_command(command="something_else", subcommand="banana", options=[])
    assert response['type'] == ResponseType.REPLY.value
    assert has_ephemeral_message(response)

    # An unknown subcommand will reply with an ephemeral channel response
    response = make_command(command="roll", subcommand="bananas", options=[])
    assert response['type'] == ResponseType.REPLY.value
    assert has_ephemeral_message(response)

    # Missing parameters will return an ephemeral channel response
    response = make_command(command="roll", subcommand="number", options=[{'name': 'min', 'value': 5}])
    assert response['type'] == ResponseType.REPLY.value
    assert has_ephemeral_message(response)


def has_ephemeral_message(response) -> bool:
    return is_ephemeral(response) and \
           type(response['data']['content']) == str and \
           len(response['data']['content']) > 0


def make_command(command: str, subcommand: str, options: typing.List[typing.Dict]) -> typing.Dict:
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
