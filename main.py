"""The bot's main entry point"""

import logging

from discordbot import DiscordBot, DiscordClient
from discordbot.config import from_env

from discordbot.notifications import NotificationsComponent
from discordbot.roles import RolesComponent


def create_components(bot: DiscordBot):
    """Configure and add components to the bot"""

    bot.add_component(NotificationsComponent, "notifications")
    bot.add_component(RolesComponent, "roles")


def main():
    """Configure and start the bot"""

    logging.basicConfig(level=logging.INFO)

    client = DiscordClient(from_env("DISCORD_TOKEN"))
    bot = DiscordBot(client)
    create_components(bot)

    bot.run()


if __name__ == "__main__":
    main()
