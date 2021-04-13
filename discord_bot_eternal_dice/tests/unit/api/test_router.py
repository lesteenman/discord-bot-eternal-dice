import json
from unittest.mock import AsyncMock

import pytest

from discord_bot_eternal_dice.api.router import RouterImpl
from discord_bot_eternal_dice.model.discord_command import DiscordCommand
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType
from discord_bot_eternal_dice.model.discord_response import DiscordResponse, ResponseType
from discord_bot_eternal_dice.model.discord_route import DiscordRoute
from discord_bot_eternal_dice.routes.ping import PingRoute
from discord_bot_eternal_dice.routes.roll import RollRoute
from discord_bot_eternal_dice.util.message_provider import MessageProvider

pytestmark = pytest.mark.asyncio


class StaticMessageProvider(MessageProvider):
    MESSAGE_UNKNOWN_COMMAND = "Invalid command"
    MESSAGE_COMMAND_USAGE = "Bad options"

    def unknown_command(self, command: DiscordCommand) -> str:
        return self.MESSAGE_UNKNOWN_COMMAND

    def command_usage(self, route: DiscordRoute) -> str:
        return self.MESSAGE_COMMAND_USAGE


async def test_handle_ping():
    # Given
    event = DiscordEvent(CommandType.PING)

    pong_response = DiscordResponse.pong()

    mock_ping_route = AsyncMock(PingRoute, autospec=True)
    mock_ping_route.call.return_value = pong_response

    router = _router(ping_route=mock_ping_route)

    # When
    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == pong_response.json()


async def test_handle_roll_number():
    # Given
    roll_response = DiscordResponse.acknowledge()

    mock_roll_route = AsyncMock(RollRoute, autospec=True)
    mock_roll_route.number.return_value = roll_response

    router = _router(roll_route=mock_roll_route)

    # When
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="number",
            options={
                'min': 1,
                'max': 2,
            }
        )
    )

    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == roll_response.json()


async def test_handle_roll_dice():
    # Given
    roll_response = DiscordResponse.acknowledge()

    mock_roll_route = AsyncMock(RollRoute, autospec=True)
    mock_roll_route.dice.return_value = roll_response

    router = _router(roll_route=mock_roll_route)

    # When
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="dice",
            options={'expression': 'd20'}
        )
    )

    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == roll_response.json()


async def test_handle_unknown_command():
    # Given
    router = _router(message_provider=StaticMessageProvider())

    # When
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="bad_command",
        )
    )

    response = await router.route(event)

    # Then
    assert response.status_code == 200
    body = json.loads(response.body)

    assert body['type'] == ResponseType.REPLY.value
    assert body['data']['content'] == StaticMessageProvider.MESSAGE_UNKNOWN_COMMAND
    assert is_ephemeral(body['data'])


@pytest.mark.parametrize('options', [
    {},  # No options at all
    {'min': 1},  # Missing 'max'
    {'max': 5},  # Missing 'min'
    {'min': 'applesauce', 'max': 5},  # Bad type
    {'min': 1, 'max': 5, 'otherwise': 20},  # Passing in an unknown option
])
async def test_handle_missing_options(options):
    # Given
    router = _router(message_provider=StaticMessageProvider())

    # When we miss one or more options
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="number",
            options=options
        )
    )

    response = await router.route(event)

    # Then
    assert response.status_code == 200
    body = json.loads(response.body)

    assert body['type'] == ResponseType.REPLY.value
    assert body['data']['content'] == StaticMessageProvider.MESSAGE_COMMAND_USAGE
    assert is_ephemeral(body['data'])


def is_ephemeral(response_data) -> bool:
    return response_data['flags'] & 64 == 64


def _router(message_provider: MessageProvider = None, roll_route: RollRoute = None, ping_route: PingRoute = None):
    if message_provider is None:
        message_provider = StaticMessageProvider()

    if ping_route is None:
        ping_route = AsyncMock(PingRoute, autospec=True)

    if roll_route is None:
        roll_route = AsyncMock(RollRoute, autospec=True)

    router = RouterImpl(
        message_provider=message_provider,
        ping_route=ping_route,
        roll_route=roll_route,
    )
    return router
