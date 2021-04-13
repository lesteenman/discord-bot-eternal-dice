from discord_bot_eternal_dice import handler
from tests.integration.utilities import make_discord_event, create_context


def test_integration_roll_numbers():
    # Try to roll a few random numbers
    roll_random_number(-50, 200)
    roll_random_number(100, 200)
    roll_random_number(1, 20)
    roll_random_number(1, 5)

    # Try a few sets of dice
    roll_dice("1d20")
    roll_dice("d10")
    roll_dice("5d20+6d6+18-1d100")


def roll_random_number(min_roll: int, max_roll: int):
    response = handler.handle_lambda(
        make_discord_event(
            command="roll",
            subcommand="number",
            options=[
                {
                    "name": "min",
                    "value": min_roll,
                },
                {
                    "name": "max",
                    "value": max_roll,
                },
            ],
        ),
        create_context()
    )

    assert response['statusCode'] == 200
    print(response['body'])


def roll_dice(expression: str):
    response = handler.handle_lambda(
        make_discord_event(
            command="roll",
            subcommand="dice",
            options=[
                {
                    "name": "expression",
                    "value": expression,
                },
            ],
        ),
        create_context()
    )

    assert response['statusCode'] == 200
    print(response['body'])
