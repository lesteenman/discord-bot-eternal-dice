import typing


class DiscordEmbed:
    def __init__(self, title: str, description: str = "", footer: str = "", color: int = None):
        self.title = title
        self.description = description
        self.footer = footer
        self.color = color

    def to_dict(self) -> typing.Dict:
        converted = {
            'title': self.title,
            'description': self.description,
            'footer': {
                'text': self.footer,
            },
            'type': 'rich',
        }

        if self.color is not None:
            converted['color'] = self.color

        return converted
