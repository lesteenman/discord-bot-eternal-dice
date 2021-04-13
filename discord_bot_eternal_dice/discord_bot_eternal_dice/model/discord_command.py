from typing import Dict


class DiscordCommand:
    def __init__(self, command_id: int, command_name: str, subcommand_name: str = None, options: Dict = None):
        self.command_id = int(command_id)
        self.command_name = command_name
        self.subcommand_name = subcommand_name

        if options is None:
            options = {}
        self.options = options


# Can only handle options with a command, a subcommand an options.
def command_from_data(event_data):
    subcommand_name = None
    options = {}

    if 'options' in event_data:
        subcommand_name = event_data['options'][0]['name']
        if 'options' in event_data['options'][0]:
            options_data = event_data['options'][0]['options']
            for option in options_data:
                options[option['name']] = option['value']

    return DiscordCommand(
        command_id=event_data['id'],
        command_name=event_data['name'],
        subcommand_name=subcommand_name,
        options=options,
    )


def _guess_command_from_data(event_data: Dict) -> DiscordCommand:
    options = {}
    for option in event_data['options']:
        options[option['name']] = option['value']

    return DiscordCommand(command_id=event_data['id'], command_name=event_data['name'], options=options)


def _create_command_from_data(event_data: Dict) -> DiscordCommand:
    command_id = event_data['id']

    sub_command = event_data['options'][0]
    command_name = sub_command['name']

    options = {}
    for option in sub_command.get('options', {}):
        options[option['name']] = option['value']

    return DiscordCommand(command_id=command_id, command_name=command_name, options=options)


def _admin_or_manage_command_from_data(event_data: Dict) -> DiscordCommand:
    command_id = event_data['id']
    command_name = event_data['options'][0]['name']

    sub_command = event_data['options'][0]['options'][0]
    subcommand_name = sub_command['name']

    options = {}
    for option in sub_command.get('options', {}):
        options[option['name']] = option['value']

    return DiscordCommand(
        command_id=command_id,
        command_name=command_name,
        subcommand_name=subcommand_name,
        options=options
    )


class UnknownCommandError(Exception):
    def __init__(self, event_data):
        super().__init__(f"Could not handle unknown command:\n{event_data}")
