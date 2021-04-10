from abc import ABC

from loguru import logger

from discord_bot_eternal_dice.errors.discord_event_disallowed_error import DiscordEventDisallowedError
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType, DiscordCommand
from discord_bot_eternal_dice.model.discord_response import DiscordResponse
from discord_bot_eternal_dice.model.lambda_response import LambdaResponse
from discord_bot_eternal_dice.routes.ping import PingRoute


class UnknownEventException(Exception):
    def __init__(self, event: DiscordEvent):
        super().__init__(f"could not handle event (type={event.type}")


class UnknownCommandException(Exception):
    def __init__(self, command: DiscordCommand):
        super().__init__(f"could not handle command (command={command.command_name}, "
                         f"subcommand={command.subcommand_name})")


class Router(ABC):
    async def route(self, event: DiscordEvent) -> LambdaResponse:
        pass


class RouterImpl(Router):
    def __init__(self, ping_route: PingRoute):
        self.ping_route = ping_route

    async def route(self, event: DiscordEvent) -> LambdaResponse:
        if event.type is CommandType.PING:
            logger.info("handling 'ping'")
            discord_response = await self.ping_route.call()

            return LambdaResponse.success(discord_response.json())

        if event.type is CommandType.COMMAND:
            try:
                discord_response = await self._handle_command(event)
                return LambdaResponse.success(discord_response.json())
            except DiscordEventDisallowedError as e:
                logger.warning(f"disallowed call detected: {e}")
                return LambdaResponse.unauthorized(str(e))

        raise UnknownEventException(event)

    async def _handle_command(self, event: DiscordEvent) -> DiscordResponse:
        pass
