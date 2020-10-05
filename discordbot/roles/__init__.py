"""A bot component that assigns roles to members"""

from discordbot import BotComponent, MessageEvent

class RolesComponent(BotComponent):
    """A bot component that assigns roles to members"""

    def __init__(self, **opts):
        super().__init__(**opts)
        # configure the component
        # access the client using `self.client`

    async def on_ready(self):
        # The client is ready to send and receive messages
        pass

    async def on_message(self, event: MessageEvent):
        # the bot received a message
        pass
