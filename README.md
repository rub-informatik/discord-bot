# Discord-Bot

## Dependency management
[Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) is used for dependency management.

To set up your environment run `pipenv sync --dev`

To start the bot: `pipenv run start`

## Configuration
Configuration is done in `main.py` and using environment variables.

Variable | Description
---------|------------
DISCORD_TOKEN | The token used to authenticate with discord

## Project structure overview
* The project's entry point is in [`main.py`](./main.py).
* The package [`discord.py`](https://pypi.org/project/discord.py/) is used to access the Discord API.
* Features of the bot are contained in "components", which are subclasses of `BotComponent` ([`discordbot/botcomponent.py`](./discordbot/botcomponent.py)).

  These feature classes are configured and added to the bot in `main.py`.
  The bot will then dispatch events from the client to the components.
