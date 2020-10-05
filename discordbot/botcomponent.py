"""Contains the base class for bot components"""

import asyncio
import inspect
import logging

from .client import DiscordClient, MessageEvent
from .eventdispatcher import EventDispatcher


class ComponentContext:
    """Contains options and utility functions for bot components"""

    def __init__(self, name: str, client: DiscordClient,
                 logger: logging.Logger, dispatcher: EventDispatcher):
        self.__dispatcher = dispatcher
        self.name = name
        self.client = client
        self.logger = logger

    def register_event_handler(self, event: str, handler):
        """Register an event handler for the specified event."""
        self.__dispatcher.register_event_handler(self, event, handler)


_EVENT_ATTR_NAME = "_discord_event_name"


def event_handler(event: str):
    """Marks a method as an event handler for the specified event.

    The method will then automatically be registered as a handler.
    """
    def decorator(handler):
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError("An event handler must be a coroutine function (async def)")

        setattr(handler, _EVENT_ATTR_NAME, event)
        return handler
    return decorator


class BotComponent:
    """A super class for bot components

    Bot components contain the logic for specific features.

    Event handling
    ==============
    To add event handlers either decorate methods with ``@event_handler("event name")``
    or use self.register_event_handler("event name", self.method).
    All event handlers must be coroutine functions (``async def``).

    Special methods
    ---------------
    There are three methods which will be registered as event handlers automatically:

    ``on_ready(self)`` (event: ready)
        Called when the client is ready

    ``on_message(self, event)``  (event: message)
        Called when a message is received

    ``shutdown(self)`` (event: shutdown)
        Called when the bot is stopping

    Creating a constructor in a subclass
    ====================================
    When creating an ``__init__``-method in a subclass,
    pass remaining keyword arguments to the super constructor::
        def __init__(self, some, args, **opts):
            super().__init__(**opts)
    """

    def __init__(self, *, component_context: ComponentContext):
        self.__context = component_context
        self.register_event_handler = component_context.register_event_handler

        # register methods marked with the event_handler decorator
        for _, value in inspect.getmembers(self):
            if inspect.ismethod(value) and hasattr(value, _EVENT_ATTR_NAME):
                event = getattr(value, _EVENT_ATTR_NAME)
                self.logger.debug("Registering method %s for event %s", value.__name__, event)
                self.register_event_handler(event, value)

        # automatically register specific methods
        if hasattr(self, "on_ready"):
            self.register_event_handler("ready", self.on_ready)
        if hasattr(self, "on_message"):
            self.register_event_handler("message", self.on_message)
        if hasattr(self, "shutdown"):
            self.register_event_handler("shutdown", self.shutdown)

    @property
    def logger(self) -> logging.Logger:
        """The logger associated to this component"""
        return self.__context.logger

    @property
    def client(self) -> DiscordClient:
        """The client of the bot"""
        return self.__context.client

    async def on_ready(self):
        """Called when the bot is ready and connected to discord"""

    async def on_message(self, event: MessageEvent):
        """Called when the bot received a message"""

    async def shutdown(self):
        """Called when the bot is shuttong down"""
