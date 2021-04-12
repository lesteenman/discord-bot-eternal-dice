import typing

import pytest

from discord_bot_eternal_dice.util.dice_roller import DiceRollerImpl


@pytest.mark.parametrize("expression", [
    "1d20",
    "d20"
])
def test_d20_roll(expression: str):
    # Given
    dice_roller = DiceRollerImpl()

    # When
    roll = dice_roller.roll(expression)

    # Then
    assert len(roll.parts) == 1
    assert roll.parts[0].dice_type == 20
    assert roll.parts[0].number == 1


@pytest.mark.parametrize("expression,value", [
    ("1", 1),
    ("0", 0),
    ("500000", 500000),
    ("-50000", -50000),
])
def test_static_roll(expression: str, value: int):
    # Given
    dice_roller = DiceRollerImpl()

    # When
    roll = dice_roller.roll(expression)

    # Then
    assert roll.result == value


@pytest.mark.parametrize("expression, dice", [
    ("1d20+3d5", {20: 1, 5: 3}),
    ("d20+6d6", {20: 1, 6: 6}),
    ("0d10+1d12", {12: 1}),
])
def test_roll_multiple_dice(expression: str, dice: typing.Dict):
    # Given
    dice_roller = DiceRollerImpl()

    # When
    roll = dice_roller.roll(expression)

    # Then
    for dice_type, number in dice.items():
        assert any(partial.number == number and partial.dice_type == dice_type for partial in roll.parts)


@pytest.mark.parametrize("expression,min_result,max_result", [
    ("1d20", 1, 20),
    ("1d20+5", 6, 25),
    ("-1d20", -20, -1),
    ("12d20+3d10-5-20-2d6", -12, 233),
])
def test_roll_result(expression: str, min_result: int, max_result: int):
    # Given
    dice_roller = DiceRollerImpl()

    for i in range(0, 5000):
        # When
        roll = dice_roller.roll(expression)

        # Then
        assert min_result <= roll.result <= max_result


