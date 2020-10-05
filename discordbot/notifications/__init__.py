"""A bot component that forwards various notifications"""

from discordbot import BotComponent

class NotificationsComponent(BotComponent):
    """A bot component that forwards various notifications"""

    def __init__(self, **opts):
        super().__init__(**opts)
        # configure the component
        # access the client using `self.client`

    async def on_ready(self):
        # The client is ready to send and receive messages
        pass
