from abc import ABC

import typing
from loguru import logger

from discord_bot_eternal_dice.errors.discord_event_disallowed_error import DiscordEventDisallowedError
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType, DiscordCommand
from discord_bot_eternal_dice.model.discord_response import DiscordResponse
from discord_bot_eternal_dice.model.discord_route import DiscordRoute
from discord_bot_eternal_dice.model.lambda_response import LambdaResponse
from discord_bot_eternal_dice.routes.ping import PingRoute
from discord_bot_eternal_dice.routes.roll import RollRoute
from discord_bot_eternal_dice.util.message_provider import MessageProvider


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
    def __init__(self, message_provider: MessageProvider, ping_route: PingRoute, roll_route: RollRoute):
        self.message_provider = message_provider
        self.ping_route = ping_route
        self.roll_route = roll_route

        self.routes = []
        self.register_routes()

    def register_routes(self):
        self.add_route(command_type=CommandType.PING, handler=self.ping_route.call)
        self.add_route(command='roll', subcommand='number',
                       options={'min': int, 'max': int}, handler=self.roll_route.number)
        self.add_route(command='roll', subcommand='dice',
                       options={'expression': str}, handler=self.roll_route.dice)

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
        for route in self.routes:
            if route.matches(event):
                if not route.validate(event.command):
                    return DiscordResponse.ephemeral_reply(self.message_provider.command_usage(route))

                return await route.handler(event)

        return DiscordResponse.ephemeral_reply(self.message_provider.unknown_command(event.command))

    def add_route(self, handler, command_type: CommandType = CommandType.COMMAND, command: str = None,
                  subcommand: str = None, options: typing.Dict = None):
        route = DiscordRoute(
            command_type=command_type,
            command=command,
            subcommand=subcommand,
            options=options,
            handler=handler
        )
        self.routes.append(route)
