import json
from unittest.mock import AsyncMock

import pytest

from discord_bot_eternal_dice.api.router import RouterImpl
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType
from discord_bot_eternal_dice.model.discord_response import DiscordResponse
from discord_bot_eternal_dice.routes.ping import PingRoute

pytestmark = pytest.mark.asyncio


async def test_handle_ping():
    # Given
    event = DiscordEvent(CommandType.PING)

    pong_response = DiscordResponse.pong()

    mock_ping_route = AsyncMock(PingRoute, autospec=True)
    mock_ping_route.call.return_value = pong_response

    # When
    router = RouterImpl(ping_route=mock_ping_route)
    response = await router.route(event)

    # Then
    assert response.status_code == 200
    assert json.loads(response.body) == pong_response.json()
