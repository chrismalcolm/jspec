"""Module for parsing JSPEC"""

import re

from constants import JSPEC_ELLIPSIS_SUBSITUTIONS
from regex import JSpec


def load(jspec_file):
    return _parse_jspec(jspec_file.read())

def loads(jspec_string):
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

    for regex, func in JSPEC_ELLIPSIS_SUBSITUTIONS.items():
        jspec_string = re.sub(regex, func, jspec_string)

    try:
        return JSpec(jspec_string)
    except Exception as exc:
        raise exc