from component import JSPEC
from matcher import match
from scanner import scan

def _decode(document):
    if not isinstance(document, str):
        raise TypeError("Object of type %s is not readbale as a JSPEC document" % document.__class__.__name__) 
    return scan(document)

def _encode(jspec):
    if not isinstance(jspec, JSPEC):
        raise TypeError("Object of type %s is not JSPEC serializable" % jspec.__class__.__name__)
    return str(jspec)

def _match(jspec, obj):
    if not isinstance(jspec, JSPEC):
        raise TypeError("Object of type %s is not a JSPEC" % obj.__class__.__name__)
    return match(jspec, obj)

def load(f):
    return loads(f.read())

def loads(document):
    return _decode(document)

def dump(obj, f):
    f.write(dumps(obj))

def dumps(obj):
    return _encode(obj)

def match(jspec, obj):
    return _match(jspec, obj)

def matchs(document, obj):
    jspec = _decode(document)
    return _match(jspec, obj)