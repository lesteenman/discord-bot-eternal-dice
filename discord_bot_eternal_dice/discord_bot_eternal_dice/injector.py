from discord_bot_eternal_dice.api.api_authorizer import ApiAuthorizerImpl
from discord_bot_eternal_dice.api.discord_event_handler import DiscordEventHandler
from discord_bot_eternal_dice.api.router import Router, RouterImpl
from discord_bot_eternal_dice.routes.ping import PingRoute
from discord_bot_eternal_dice.routes.roll import RollRouteImpl
from discord_bot_eternal_dice.util.dice_roller import DiceRoller, DiceRollerImpl
from discord_bot_eternal_dice.util.message_provider import MessageProviderImpl, MessageProvider


def discord_event_handler():
    return DiscordEventHandler(
        router=_router(),
        api_authorizer=_api_authorizer()
    )


def _router() -> Router:
    message_provider = _message_provider()
    dice_roller = _dice_roller()

    ping_route = _ping_route()
    roll_route = _roll_route(
        message_provider=message_provider,
        dice_roller=dice_roller,
    )

    return RouterImpl(
        message_provider=message_provider,
        roll_route=roll_route,
        ping_route=ping_route,
    )


def _ping_route():
    return PingRoute()


def _roll_route(message_provider: MessageProvider, dice_roller: DiceRoller):
    return RollRouteImpl(
        message_provider=message_provider,
        dice_roller=dice_roller,
    )


def _message_provider():
    return MessageProviderImpl()


def _dice_roller():
    return DiceRollerImpl()


def _api_authorizer():
    return ApiAuthorizerImpl()
