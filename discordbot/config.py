"""Utilities for configuration"""

import os
import sys

# loading .env is normally done by pipenv, but not when running in PyCharm
from dotenv import load_dotenv
load_dotenv()


def from_env(name: str, *, default=None, optional=False, type_=str):
    """Get a configuration value from the environment

    :param name:
        The name of the environment variable
    :param default:
        The default value which should be used if the variable is not set
    :param optional:
        If the default value is None and the variable is not set, return None
    :param type_:
        The type of the value

    Example: To get an int from the environment:
    >>> from_env("SOME_INT", type_=int)
    """

    if __debug__ and not name.isupper():
        raise ValueError("Names of environment variables should be upper case by convention")

    value = os.getenv(name)

    if value is None:
        if optional:
            return default

        print(
            ("Missing environment variable {0}.\n" +
             "Create a .env-File containing {0}=<value> to configure it.").format(name),
            file=sys.stderr,
        )
        sys.exit(1)

    return type_(value)
