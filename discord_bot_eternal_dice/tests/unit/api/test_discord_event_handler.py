import json
from typing import Dict, Optional
from unittest.mock import patch

from discord_bot_eternal_dice.api.api_authorizer import ApiAuthorizer, AuthorizationResult
from discord_bot_eternal_dice.api.discord_event_handler import DiscordEventHandler
from discord_bot_eternal_dice.api.router import Router
from discord_bot_eternal_dice.model import discord_event
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType
from discord_bot_eternal_dice.model.lambda_response import LambdaResponse


class _TestAuthorizer(ApiAuthorizer):
    def __init__(self, result: AuthorizationResult, response: Optional[LambdaResponse]):
        self.result = result
        self.response = response

    def authorize(self, event: Dict) -> (AuthorizationResult, LambdaResponse):
        return self.result, self.response


class _TestRouter(Router):
    def __init__(self, response: Optional[LambdaResponse]):
        self.response = response

    async def route(self, event: DiscordEvent) -> LambdaResponse:
        return self.response


def test_unauthorized_request():
    # Given
    test_authorizer = _TestAuthorizer(AuthorizationResult.FAIL,
                                      LambdaResponse.unauthorized("key does not check out"))

    body = {'type': 1}
    event = {
        'body': json.dumps(body),
        'headers': {
            'x-signature-ed25519': '',
            'x-signature-timestamp': '',
        }
    }

    # When
    discord_event_handler = DiscordEventHandler(router=_TestRouter(None),
                                                api_authorizer=test_authorizer)
    response = discord_event_handler.handle(event)

    # Then
    assert response['statusCode'] == 401


@patch.object(discord_event, 'from_event', autospec=True)
def test_authorized_request(mock_from_event):
    # Given
    test_authorizer = _TestAuthorizer(AuthorizationResult.PASS, None)
    test_router = _TestRouter(LambdaResponse.success({'response': 'mocked'}))

    mock_from_event.return_value = None

    event = {
        'body': json.dumps({'type': 1}),
        'headers': {
            'x-signature-ed25519': '',
            'x-signature-timestamp': '',
        }
    }

    # When
    discord_event_handler = DiscordEventHandler(router=test_router,
                                                api_authorizer=test_authorizer)
    response = discord_event_handler.handle(event)

    # Then
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'response': 'mocked'}


@patch.object(discord_event, 'from_event', autospec=True)
def test_discord_event(mock_from_event):
    # Given
    test_authorizer = _TestAuthorizer(AuthorizationResult.PASS, None)

    test_router = _TestRouter(LambdaResponse.success({'response': 'mocked'}))

    event_body = {'type': 1}

    discord_event = DiscordEvent(CommandType.COMMAND)
    mock_from_event.return_value = discord_event

    event = {
        'body': json.dumps(event_body),
        'headers': {
            'x-signature-ed25519': '',
            'x-signature-timestamp': '',
        }
    }

    # When
    discord_event_handler = DiscordEventHandler(router=test_router,
                                                api_authorizer=test_authorizer)
    response = discord_event_handler.handle(event)

    # Then
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'response': 'mocked'}
