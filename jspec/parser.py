"""Module for parsing JSPEC."""

import re

from jspec import constants
from jspec import error
from jspec import jregex


def load(jspec_file):
    """Load the JSPEC as a readable file."""
    return _parse_jspec(jspec_file.read())

def loads(jspec_string):
    """Load the JSPEC as a jspec string."""
    return _parse_jspec(jspec_string)

def _parse_jspec(jspec_string):
    """
        Parses the 'jspec_string' as a JSPEC file string.

        Parameters:
        > jspec_string (str): string of a JSPEC
        
        Returns:
        > jspec (JSpec)

        Raises:
        > JSpecLoadError
    """
    jspec_string = jspec_string.replace("\n", "").replace("\\", "\\\\")

    for regex, func in constants.JSPEC_ELLIPSIS_SUBSTITUTIONS.items():
        jspec_string = re.sub(regex, func, jspec_string)

    try:
        return jregex.JSpec(jspec_string)
    except error.JSpecLoadError as jle:
        raise jle