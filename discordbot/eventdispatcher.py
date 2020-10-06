"""Handles dispatching of events

This module is used by DiscordBot and DiscordClient
to dispatch lifecycle events and events received by the discord client.
"""

import asyncio
from .client import MessageEvent


async def _call_handler(source, handler, event, *args, **kwargs):
    """Call the handler and catch any errors"""
    try:
        await handler(*args, **kwargs)
    # pylint: disable=broad-except
    except Exception as exc:
        source.logger.exception("Exception while handling event %s: %s", event, exc)


async def _handle_event(event, handlers, args, kwargs):
    """Call each handler with the specified arguments"""
    coros = [_call_handler(source, handler, event, *args, **kwargs) for source, handler in handlers]
    await asyncio.wait(coros)


class EventDispatcher:
    """Dispatches events to their handlers"""

    def __init__(self):
        self.__event_handlers = {}

    def register_event_handler(self, source, event: str, handler):
        """Register an event handler for the specified event."""
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError("An event handler must be a coroutine fuction (async def)")

        handlers = self.__event_handlers.get(event)
        if handlers is None:
            self.__event_handlers[event] = {(source, handler)}
        else:
            handlers.add((source, handler))

    def dispatch_event(self, event: str, *args, **kwargs) -> asyncio.Task:
        """Dispatch an event to its handlers."""
        handlers = self.__event_handlers.get(event)
        if handlers is None:
            return None

        return asyncio.create_task(
            _handle_event(event, handlers, args, kwargs),
            name="discord_event_handler:" + event
        )

    async def dispatch_event_async(self, event: str, *args, **kwargs):
        """Dispatch an event and wait for its task"""
        task = self.dispatch_event(event, *args, **kwargs)
        if task is not None:
            await task

    async def dispatch_message(self, event: MessageEvent):
        """Dispatch a message event to its handlers"""
        handlers = self.__event_handlers.get("message")
        if handlers is None:
            return

        for source, handler in handlers:
            await _call_handler(source, handler, "message", event)
            if event.claimed:
                break
