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

### Example `.env`-file

You can configure environment variables by creating a `.env`-file in the project's root directory.

```sh
# Discord API token
DISCORD_TOKEN="<put your token here>"
```

## Project structure overview
* The project's entry point is in [`main.py`](./main.py).
* The package [`discord.py`](https://pypi.org/project/discord.py/) is used to access the Discord API.
* Features of the bot are contained in "components", which are subclasses of `BotComponent` ([`discordbot/botcomponent.py`](./discordbot/botcomponent.py)).

  These component classes are configured and added to the bot in `create_components` in [`main.py`](./main.py).
  The client will then dispatch all events to the components.

### Components

* [`NotificationsComponent`](./discordbot/notifications/__init__.py) (in [`discordbot/notifications/`](./discordbot/notifications/))
* [`RolesComponent`](./discordbot/roles/__init__.py) (in [`discordbot/roles/`](./discordbot/notifications/))
