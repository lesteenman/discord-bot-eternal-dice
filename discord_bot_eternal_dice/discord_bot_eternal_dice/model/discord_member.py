from typing import Dict


class DiscordMember:
    def __init__(self, username: str = None, user_id: int = None, nickname: str = None):
        self.username = username
        self.user_id = user_id
        self.nickname = nickname

    @property
    def name(self):
        if self.nickname is not None:
            return self.nickname
        return self.username


def member_from_data(member_data: Dict) -> DiscordMember:
    return DiscordMember(
        username=member_data['user']['username'],
        user_id=int(member_data['user']['id']),
        nickname=member_data['nick'],
    )
