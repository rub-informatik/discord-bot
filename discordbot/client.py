"""Contains the class ``DiscordClient``"""

import discord


class DiscordClient(discord.Client):
    """The Discord API client

    This class manages the bot's connection to discord and dispatches events to components."""

    def __init__(self, token: str):
        super().__init__()
        self.dispatcher = None
        self.__token = token

    # pylint: disable=arguments-differ
    async def start(self):
        """Start the client."""
        if self.dispatcher is None:
            raise Exception("The client needs to be attached to a bot first")
        await super().start(self.__token)

    def dispatch(self, event, *args, **kwargs):
        super().dispatch(event, *args, **kwargs)

        if event != "message":
            self.dispatcher.dispatch_event(event, *args, **kwargs)

    async def on_message(self, message: discord.Message):
        """Handle incoming messages"""
        if message.author == self.user:
            return

        event = MessageEvent(message)
        await self.dispatcher.dispatch_message(event)


class MessageEvent:
    """The event dispatched to bot components when a message is received"""

    def __init__(self, message: discord.Message):
        self.claimed = False
        self.message = message
        self.content = message.content
        self.author = message.author
        self.channel = message.channel

    def is_private_channel(self):
        """Return whether the message is sent in a private message channel"""
        return self.message.channel.type == discord.ChannelType.private

    def claim(self):
        """Claims the event for the current handler.

        The event won't be dispatched to other handlers afterwards.
        """
        self.claimed = True

    async def respond(self, *args, **kwargs):
        """Respond to the message"""
        await self.channel.send(*args, **kwargs)

    async def respond_error(self, message):
        """Notify the sender that what they sent was invalid"""
        await self.author.send(message)
