from decode import _decode
from encode import _encode

def load(f):
    return loads(f.read())

def loads(document):
    return _decode(document)

def dump(obj, f):
    f.write(dumps(obj))

def dumps(obj):
    return _encode(obj)