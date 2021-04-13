import random
from abc import ABC

from discord_bot_eternal_dice.model.discord_event import DiscordEvent
from discord_bot_eternal_dice.model.discord_response import DiscordResponse
from discord_bot_eternal_dice.util.dice_roller import DiceRoller
from discord_bot_eternal_dice.util.message_provider import MessageProvider


class RollRoute(ABC):
    async def number(self, event: DiscordEvent) -> DiscordResponse:
        pass

    async def dice(self, event: DiscordEvent) -> DiscordResponse:
        pass


class RollRouteImpl(RollRoute):
    def __init__(self, message_provider: MessageProvider, dice_roller: DiceRoller):
        self.message_provider = message_provider
        self.dice_roller = dice_roller

    async def number(self, event: DiscordEvent) -> DiscordResponse:
        min_roll = event.command.options['min']
        max_roll = event.command.options['max']
        random_number = random.randint(min_roll, max_roll)

        message = self.message_provider.roll_number(
            member_name=event.member.name,
            roll_min=min_roll,
            roll_max=max_roll,
            number=random_number,
        )

        return DiscordResponse.reply(content=message)

    async def dice(self, event: DiscordEvent) -> DiscordResponse:
        expression = event.command.options['expression']

        dice_roll = self.dice_roller.roll(expression)
        message = self.message_provider.roll_dice(
            member_name=event.member.name,
            dice_roll=dice_roll,
        )

        return DiscordResponse.reply(content=message)
