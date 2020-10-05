"""Contains the class ``DiscordBot``"""

import logging
from typing import Iterator

from .botcomponent import BotComponent, ComponentContext
from .client import DiscordClient
from .eventdispatcher import EventDispatcher


class DiscordBot:
    """The class containing the bot's main logic."""

    def __init__(self, client: DiscordClient):
        self.__logger = logging.getLogger("discordbot")
        self.__components = []
        self.__dispatcher = EventDispatcher()

        client.dispatcher = self.__dispatcher
        self.client = client

    @property
    def components(self) -> Iterator[BotComponent]:
        """An iterator for all the components added to this bot."""
        return iter(self.__components)

    def run(self):
        """Start the discord bot."""

        loop = self.client.loop
        try:
            loop.run_until_complete(self.client.start())
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self.__dispatcher.dispatch_event_async("shutdown"))
            loop.run_until_complete(self.client.close())
            loop.close()

    def add_component(self, cls, name, *args, **kwargs):
        """Add a component to the bot.

        cls
            The class of the component
        name
            The name used to identify the component
        """
        if self.client.is_ready():
            raise ValueError("Components should be added ")

        context = ComponentContext(
            name=name,
            client=self.client,
            logger=self.__logger.getChild(name),
            dispatcher=self.__dispatcher
        )
        component = cls(*args, **kwargs, component_context=context)
        self.__components.append(component)
