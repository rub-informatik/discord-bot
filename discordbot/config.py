"""Utilities for configuration"""

import os
import sys


def from_env(name: str, *, default=None, optional=False, type_=str):
    """Get a configuration value from the environment"""

    if __debug__ and not name.upper():
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
