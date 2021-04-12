from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from discord_bot_eternal_dice.discord_messaging import DiscordMessaging
from discord_bot_eternal_dice.model.dice_roll import DiceRoll
from discord_bot_eternal_dice.model.discord_command import DiscordCommand
from discord_bot_eternal_dice.model.discord_event import DiscordEvent, CommandType
from discord_bot_eternal_dice.model.discord_member import DiscordMember
from discord_bot_eternal_dice.routes import roll
from discord_bot_eternal_dice.routes.roll import RollRouteImpl
from discord_bot_eternal_dice.util.dice_roller import DiceRoller
from discord_bot_eternal_dice.util.message_provider import MessageProvider

pytestmark = pytest.mark.asyncio


@patch.object(roll.random, 'randint')
@pytest.mark.parametrize("roll_min,roll_max", [
    (1, 6),
    (20, 100),
    (-50, 600),
])
async def test_roll_number(mock_random_int, roll_min: int, roll_max: int):
    # Given
    channel_id = 10
    member_name = "Ion"
    rolled_number = 6  # Rolled a dice for this, guaranteed to be random.
    generated_message = "Ion rolled a 6!"

    mock_message_provider = MagicMock(MessageProvider)
    mock_message_provider.roll_number.return_value = generated_message

    mock_discord_messaging = AsyncMock(DiscordMessaging)

    roll_route = RollRouteImpl(
        message_provider=mock_message_provider,
        discord_messaging=mock_discord_messaging,
        dice_roller=FakeDiceRoller(-1),
    )

    # And we get a fixed return value (does not matter if it's actually in the range)
    mock_random_int.return_value = rolled_number

    # When
    event = DiscordEvent(
        command_type=CommandType.COMMAND,
        channel_id=channel_id,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="number",
            options={
                'min': roll_min,
                'max': roll_max,
            }
        ),
        member=DiscordMember(
            nickname=member_name,
        )
    )
    await roll_route.number(event)

    # Then a random number was called
    mock_random_int.assert_called_with(roll_min, roll_max)

    # And the message was generated correctly
    mock_message_provider.roll_number.assert_called_with(
        member_name=member_name,
        roll_min=roll_min,
        roll_max=roll_max,
        number=rolled_number,
    )

    # And the message was sent to the correct channel
    mock_discord_messaging.send_channel_message.assert_called_with(
        channel_id=channel_id,
        text=generated_message,
    )


class FakeDiceRoller(DiceRoller):
    def __init__(self, diceroll: DiceRoll):
        self.diceroll = diceroll

    def roll(self, expression: str) -> DiceRoll:
        return self.diceroll


async def test_roll_dice():
    # Given
    channel_id = 10
    member_name = "Charles"
    dice_expression = "1d6+100"
    generated_message = "Charles rolled 1d6+100: it's a 6!"

    dice_roll = DiceRoll(dice_expression)

    mock_message_provider = MagicMock(MessageProvider)
    mock_message_provider.roll_dice.return_value = generated_message

    mock_discord_messaging = AsyncMock(DiscordMessaging)

    roll_route = RollRouteImpl(
        message_provider=mock_message_provider,
        discord_messaging=mock_discord_messaging,
        dice_roller=FakeDiceRoller(dice_roll),
    )

    # When
    event = DiscordEvent(
        command_type=CommandType.COMMAND,
        channel_id=channel_id,
        command=DiscordCommand(
            command_id=-1,
            command_name="roll",
            subcommand_name="dice",
            options={
                'expression': dice_expression,
            }
        ),
        member=DiscordMember(
            nickname=member_name,
        )
    )
    await roll_route.dice(event)

    # Then the message was generated correctly
    mock_message_provider.roll_dice.assert_called_with(
        member_name=member_name,
        dice_roll=dice_roll,
    )

    # And the message was sent to the correct channel
    mock_discord_messaging.send_channel_message.assert_called_with(
        channel_id=channel_id,
        text=generated_message,
    )
