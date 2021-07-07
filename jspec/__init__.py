"""Jspec Module"""

__version__ = "0.0.1"

from jspec.parser import load, loads
from jspec.constants import (
    JSPEC_ELLIPSIS_SUBSTITUTIONS,
    JSPEC_OBJECT_ITEMS_SUBSTITUTION, 
    JSPEC_OBJECT_TEMPLATE_VALUE, 
    JSPEC_ARRAY_ELEMENT_SUBSTITUTION, 
    JSPEC_ARRAY_TEMPLATE_VALUE
)
from jspec.error import JSpecError, JSpecLoadError
from jspec.jregex import JSpec
from jspec.result import Result