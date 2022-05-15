"""Exported functions for the jspec module.
"""

from . import scanner
from . import matcher
from . import entity

__version__ = "2.1.2"

def _decode(document, pretty=False, indent=None):
    if not isinstance(document, str):
        raise TypeError("Expecting a string not %s" % document.__class__)
    return scanner.scan(document, pretty=pretty, indent=indent)

def _encode(spec):
    if not isinstance(spec, entity.JSPEC):
        raise TypeError("Expecting a JSPEC not %s" % spec.__class__) 
    return str(spec)

def _match(spec, element):
    if not isinstance(spec, entity.JSPEC):
        raise TypeError("Expecting a JSPEC not %s" % spec.__class__) 
    return matcher.match(spec, element)

def load(file, pretty=False, indent=None):
    """Loads the file ``file`` as a JSPEC.
    
    Args:
        file (file): File to be loaded as a JSPEC. Must support the read
            method.
        pretty (bool): Optional. Default is False, if True the JSPEC string
            will be formated with tabs, newlines and retain any comments
        indent (str/None): Optional. The tab indentation for the pretty format
            for the JSPEC. None means a default tab will be used.
    
    Returns:
        jspec.JSPEC: The JSPEC instance created from the file loaded.

    Raises:
        TypeError: If unable to load the file contents as a string or if the
            indent is not consisting only of tabs and spaces.
        jspec.JSPECDecodeError: Any error with decoding the file contents as a
            JSPEC.
    """
    return loads(file.read(), pretty=pretty, indent=indent)

def loads(document, pretty=False, indent=None):
    """Loads the string ``document`` as a JSPEC.
    
    Args:
        document (str): String to be loaded as a JSPEC.
        pretty (bool): Optional. Default is False, if True the JSPEC string
            will be formated with tabs, newlines and retain any comments
        indent (str/None): Optional. The tab indentation for the pretty format
            for the JSPEC. None means a default tab will be used.
    
    Returns:
        jspec.JSPEC: The JSPEC instance created from the string loaded.

    Raises:
        TypeError: If the input is not a string or if the indent is not
            consisting only of tabs and spaces.
        jspec.JSPECDecodeError: Any error with decoding the string as a JSPEC.
    """
    return _decode(document, pretty=pretty, indent=indent)

def dump(spec, file):
    """Dump the serialization of the JSPEC ``spec`` into the file ``file``.

    Args:
        spec (jspec.JSPEC): The JSPEC instance to dump.
        file (file): File to be written as a JSPEC. Must support the write
            method.
    
    Raises:
        TypeError: If the input for ``spec`` is not a jspec.JSPEC.
    """
    file.write(dumps(spec))

def dumps(spec):
    """Returns the serialization of the JSPEC ``spec``.

    Args:
        spec (jspec.JSPEC): The JSPEC instance to dump.

    Returns:
        str: The serialization of ``spec``.
    
    Raises:
        TypeError: If the input for ``spec`` is not a jspec.JSPEC.
    """
    return _encode(spec)

def check(spec, element):
    """Determine if the Python native JSON object ``element`` is a good match
    for the JSPEC ``spec``.

    Args:
        spec (jspec.JSPEC): The JSPEC instance to attempt to match.
        element (obj): The Python native JSON object to attempt to match.

    Returns:
        bool: Whether ``element`` is a good match for ``spec``.
        str: If it was a bad match, the reason why the match failed.

    Raises:
        TypeError: If the input for ``spec`` is not a jspec.JSPEC.
        ValueError: If ``spec`` contains any unsupported classes
    """
    return _match(spec, element)

def checks(document, element):
    """Determine if the Python native JSON object ``element`` is a good match
    for the JSPEC formed when loading ``document``.

    Args:
        document (sre): The document of the JSPEC to attempt to match.
        element (obj): The Python native JSON object to attempt to match.

    Returns:
        bool: Whether ``element`` is a good match for the JSPEC formed when
            loading ``document``.
        str: If it was a bad match, the reason why the match failed.

    Raises:
        TypeError: If the input for ``document`` is not a string.
        ValueError: If ``spec`` contains any unsupported classes
    """
    spec = _decode(document)
    return _match(spec, element)