from discord_bot_eternal_dice.model.discord_response import DiscordResponse


class PingRoute:
    async def call(self) -> DiscordResponse:
        return DiscordResponse.pong()
