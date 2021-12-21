# TODO Add documentation here
# TODO Set as version 1.2.0 as beta
# TODO See how to get github badges
# TODO deploy as module

from . import scanner
from . import matcher
from . import component

__version__ = "1.1.0"

def _decode(document):
    if not isinstance(document, str):
        raise TypeError("Expecting a string not %s" % document.__class__)
    return scanner.scan(document)

def _encode(spec):
    if not isinstance(spec, component.JSPEC):
        raise TypeError("Expecting a JSPEC not %s" % spec.__class__) 
    return str(spec)

def _match(spec, element):
    if not isinstance(spec, component.JSPEC):
        raise TypeError("Expecting a JSPEC not %s" % spec.__class__) 
    return matcher.match(spec, element)

def load(f):
    return loads(f.read())

def loads(document):
    return _decode(document)

def dump(spec, f):
    f.write(dumps(spec))

def dumps(spec):
    return _encode(spec)

def check(spec, element):
    return _match(spec, element)

def checks(document, element):
    spec = _decode(document)
    return _match(spec, element)