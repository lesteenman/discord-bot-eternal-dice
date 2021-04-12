import json
from unittest.mock import AsyncMock

import pytest

from discord_bot_eternal_dice.api.router import RouterImpl
from discord_bot_eternal_dice.model.discord_command import DiscordCommand
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType
from discord_bot_eternal_dice.model.discord_response import DiscordResponse
from discord_bot_eternal_dice.routes.ping import PingRoute
from discord_bot_eternal_dice.routes.roll import RollRoute

pytestmark = pytest.mark.asyncio


async def test_handle_ping():
    # Given
    event = DiscordEvent(CommandType.PING)

    pong_response = DiscordResponse.pong()

    mock_ping_route = AsyncMock(PingRoute, autospec=True)
    mock_ping_route.call.return_value = pong_response

    # When
    router = RouterImpl(
        ping_route=mock_ping_route,
        roll_route=AsyncMock(RollRoute),
    )
    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == pong_response.json()


async def test_handle_roll_number():
    # Given
    roll_response = DiscordResponse.acknowledge()

    mock_roll_route = AsyncMock(RollRoute, autospec=True)
    mock_roll_route.number.return_value = roll_response

    # When
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="number",
        )
    )

    router = RouterImpl(ping_route=AsyncMock(PingRoute), roll_route=mock_roll_route)
    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == roll_response.json()


async def test_handle_roll_dice():
    # Given
    roll_response = DiscordResponse.acknowledge()

    mock_roll_route = AsyncMock(RollRoute, autospec=True)
    mock_roll_route.dice.return_value = roll_response

    # When
    event = DiscordEvent(
        CommandType.COMMAND,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="dice",
        )
    )

    router = RouterImpl(ping_route=AsyncMock(PingRoute), roll_route=mock_roll_route)
    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == roll_response.json()
