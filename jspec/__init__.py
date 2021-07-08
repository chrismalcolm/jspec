"""Jspec Module"""

__version__ = "0.1.0"

from jspec.parser import load, loads
from jspec.error import JSpecError, JSpecLoadError
from jspec.jregex import JSpec
from jspec.result import Result