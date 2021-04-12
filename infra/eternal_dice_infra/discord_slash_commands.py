from typing import Dict

import requests

COMMAND_OPTION_TYPE_SUB_COMMAND = 1
COMMAND_OPTION_TYPE_SUB_COMMAND_GROUP = 2
COMMAND_OPTION_TYPE_STRING = 3
COMMAND_OPTION_TYPE_INTEGER = 4
COMMAND_OPTION_TYPE_BOOLEAN = 5
COMMAND_OPTION_TYPE_USER = 6
COMMAND_OPTION_TYPE_CHANNEL = 7
COMMAND_OPTION_TYPE_ROLE = 8


commands = [
    {
        "name": "roll",
        "description": "Commands to generate random numbers.",
        "options": [
            {
                "name": "number",
                "description": "Roll a random number between a min and max value.",
                "type": COMMAND_OPTION_TYPE_SUB_COMMAND,
                "options": [
                    {
                        "name": "min",
                        "description": "The minimum roll.",
                        "type": COMMAND_OPTION_TYPE_INTEGER,
                        "required": True,
                    },
                    {
                        "name": "min",
                        "description": "The maximum roll.",
                        "type": COMMAND_OPTION_TYPE_INTEGER,
                        "required": True,
                    }
                ],
            },
            {
                "name": "dice",
                "description": "Roll some random dice!",
                "type": COMMAND_OPTION_TYPE_SUB_COMMAND,
                "options": [
                    {
                        "name": "game-id",
                        "description": "The ID of the Eternal Guess game. If omitted, will generate a random ID.",
                        "type": COMMAND_OPTION_TYPE_STRING,
                        "required": False,
                    }
                ],
            },
        ]
    },
]


def register():
    pass


def delete_command(command_id: int, config: Dict):
    print("Deleting application command")
    url = "https://discord.com/api/v8/applications/{}/commands/{}".format(
        config['DISCORD_APPLICATION_ID'],
        command_id
    )

    headers = {
        "Authorization": f"Bot {config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.delete(url, headers=headers)
    if response.status_code > 201:
        raise Exception(f"unexpected status_code {response.status_code} received: '{response.text}'")


def create_command(command: Dict, config: Dict):
    print("Creating application command")
    url = "https://discord.com/api/v8/applications/{}/commands".format(
        config['DISCORD_APPLICATION_ID'],
    )

    headers = {
        "Authorization": f"Bot {config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.post(url, headers=headers, json=command)
    print(response.text)
    if response.status_code > 201:
        raise Exception(f"unexpected status_code {response.status_code} received: '{response.text}'")
