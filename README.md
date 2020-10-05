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
