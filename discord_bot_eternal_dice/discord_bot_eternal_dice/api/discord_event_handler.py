import asyncio
import json
from typing import Dict

from discord_bot_eternal_dice.api.api_authorizer import ApiAuthorizer, AuthorizationResult
from discord_bot_eternal_dice.api.router import Router
from discord_bot_eternal_dice.model import discord_event


class DiscordEventHandler:
    def __init__(self, router: Router, api_authorizer: ApiAuthorizer):
        self.router = router
        self.api_authorizer = api_authorizer

    def handle(self, event) -> Dict:
        result, response = self.api_authorizer.authorize(event)
        if result == AuthorizationResult.PASS:
            body_json = json.loads(event['body'])
            event = discord_event.from_event(body_json)

            response = asyncio.get_event_loop() \
                .run_until_complete(self.router.route(event))

        return response.json()
