"""The bot's main entry point"""

import logging

from discordbot import DiscordBot, DiscordClient
from discordbot.config import from_env

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = DiscordClient(from_env("DISCORD_TOKEN"))
    bot = DiscordBot(client)
    bot.run()
