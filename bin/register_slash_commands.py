#!/usr/bin/env python3
import json
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


def register(config: Dict):
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
                            "name": "max",
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
                            "name": "expression",
                            "description": "The dice expression, like '1d20+5'.",
                            "type": COMMAND_OPTION_TYPE_STRING,
                            "required": False,
                        }
                    ],
                },
            ]
        },
    ]

    for command in commands:
        create_command(command, config)


def get_config():
    with open('app_config.json', 'r') as config_file:
        return json.loads(config_file.read())


def delete_guild_command(command_id: int, config: Dict, guild_name: str):
    print("Creating guild command")
    url = "https://discord.com/api/v8/applications/{}/guilds/{}/commands/{}".format(
        config['DISCORD_APPLICATION_ID'],
        config[guild_name.upper() + '_GUILD_ID'],
        command_id
    )

    headers = {
        "Authorization": f"Bot {config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.delete(url, headers=headers)
    if response.status_code > 201:
        raise Exception(f"unexpected status_code {response.status_code} received: '{response.text}'")


def create_guild_command(command: Dict, config: Dict, guild_name: str):
    print("Creating guild command")
    url = "https://discord.com/api/v8/applications/{}/guilds/{}/commands".format(
        config['DISCORD_APPLICATION_ID'],
        config[guild_name.upper() + '_GUILD_ID'],
    )

    headers = {
        "Authorization": f"Bot {config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.post(url, headers=headers, json=command)
    print(response.text)
    if response.status_code > 201:
        raise Exception(f"unexpected status_code {response.status_code} received: '{response.text}'")


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


if __name__ == "__main__":
    register(get_config())
