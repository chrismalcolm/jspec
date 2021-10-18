from component import JSPEC

def _encode(obj):
    if not isinstance(obj, JSPEC):
        raise TypeError("Object of type %s is not JSPEC serializable" % obj.__class__.__name__)
    return str(obj._element)