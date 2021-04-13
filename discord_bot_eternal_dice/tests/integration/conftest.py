from typing import Dict

import pytest
from loguru import logger

from discord_bot_eternal_dice.api.api_authorizer import ApiAuthorizer, AuthorizationResult
from discord_bot_eternal_dice.discord_messaging import DiscordMessaging
from discord_bot_eternal_dice.model.discord_member import DiscordMember
from discord_bot_eternal_dice.model.lambda_response import LambdaResponse


@pytest.fixture(autouse=True)
def fixed_authorization_result(mocker):
    class PassingTestAuthorizer(ApiAuthorizer):
        @staticmethod
        def authorize(event: Dict) -> (AuthorizationResult, LambdaResponse):
            return AuthorizationResult.PASS, None

    test_authorizer = PassingTestAuthorizer()
    mocker.patch('discord_bot_eternal_dice.injector._api_authorizer', return_value=test_authorizer)


@pytest.fixture(autouse=True)
def stub_discord_messaging(mocker):
    class SilentDiscordMessaging(DiscordMessaging):
        async def send_channel_message(self, channel_id: int, text: str) -> int:
            logger.info(f"[stub send_channel_emssage] channel_id={channel_id}, text={text}")
            return 1

        async def update_channel_message(self, channel_id: int, message_id: int, text: str):
            logger.info(f"[stub update_channel_emssage] channel_id={channel_id}, message_id={message_id} text={text}")
            pass

        async def send_dm(self, member: DiscordMember, text: str):
            logger.info(f"[stub send_dm] member_id={member.user_id} text={text}")
            pass

    # silent_discord_messaging = SilentDiscordMessaging()
    # mocker.patch('discord_bot_eternal_dice.injector._discord_messaging', return_value=silent_discord_messaging)
