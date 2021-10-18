import re

class JSPEC:

    def __init__(self, element):
        self.element = element

class JSPECElement:

    def __init__(self):
        self.spec = None
        self.string = ""

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

class JSPECObject(JSPECElement):
    
    def __init__(self, pairs):
        self.spec = dict(pairs)
        self.string = str(self.spec)

class JSPECArray(JSPECElement):
    
    def __init__(self, values):
        self.spec = values
        self.string = str(values)

class JSPECString(JSPECElement):
    
    def __init__(self, value):
        self.spec = value
        self.string = '"%s"' % value

class JSPECInt(JSPECElement):
    
    def __init__(self, value):
        self.spec = int(value)
        self.string = str(value)

class JSPECReal(JSPECElement):
    
    def __init__(self, value):
        self.spec = float(value)
        self.string = str(value)

class JSPECBoolean(JSPECElement):
    
    def __init__(self, value):
        self.spec = bool(value)
        self.string = "true" if self.spec else "false"

class JSPECWildcard(JSPECElement):
    
    def __init__(self):
        self.spec = None
        self.string = '...'

class JSPECNull(JSPECElement):
    
    def __init__(self):
        self.spec = None
        self.string = "null"


class JSPECCapture:

    def __init__(self):
        self.element = None
        self.string = ""

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

class JSPECArrayCaptureElement(JSPECCapture):
    
    def __init__(self, element):
        self.element = element
        self.string = '<%s>' % str(element)

class JSPECObjectCaptureKey(JSPECCapture):

    def __init__(self, element):
        self.element = element
        self.string = '<%s' % str(element)

class JSPECObjectCaptureValue(JSPECCapture):

    def __init__(self, element):
        self.element = element
        self.string = '%s>' % str(element)