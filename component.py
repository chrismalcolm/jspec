class JSPEC:

    def __init__(self, element):
        self.element = element


class JSPECElement:
    PLACEHOLDER = ""
    SPEC_FUNC   = lambda x: None
    SERIALIZER  = lambda x: ""
    
    def __init__(self, value, is_placeholder=False):
        self.spec = self.SPEC_FUNC(value)
        self.string = self.SERIALIZER(value) if not is_placeholder else self.PLACEHOLDER
        self.is_placeholder = is_placeholder

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.is_placeholder and other.is_placeholder:
            return True
        if self.is_placeholder or other.is_placeholder:
            return False
        return self.spec == other.spec

class JSPECObject(JSPECElement):  
    PLACEHOLDER = "object"
    SPEC_FUNC   = dict
    SERIALIZER   = lambda pairs: str(dict(pairs))

class JSPECArray(JSPECElement):
    PLACEHOLDER = "array"
    SPEC_FUNC   = list
    SERIALIZER  = str

class JSPECString(JSPECElement):
    PLACEHOLDER = "string"
    SPEC_FUNC   = str
    SERIALIZER  = lambda val: '"%s"' % val

class JSPECInt(JSPECElement):
    PLACEHOLDER = "imt"
    SPEC_FUNC   = int
    SERIALIZER  = str

class JSPECReal(JSPECElement):
    PLACEHOLDER = "real"
    SPEC_FUNC   = float
    SERIALIZER  = str

class JSPECBoolean(JSPECElement):
    PLACEHOLDER = "bool"
    SPEC_FUNC   = bool
    SERIALIZER  = lambda val: "true" if bool(val) else "false"

class JSPECNull(JSPECElement):
    SPEC_FUNC   = lambda val: None
    SERIALIZER  = lambda val: "null"

class JSPECWildcard(JSPECElement):
    SPEC_FUNC   = lambda val: None
    SERIALIZER  = lambda val: "*"


class JSPECCapture:
    SERIALIZER = lambda element: ""
    ELLIPSIS   = ""

    def __init__(self, element, is_ellipsis=False):
        self.element = element
        self.string = self.SERIALIZER(element) if not is_ellipsis else self.ELLIPSIS

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.element == other.element

class JSPECArrayCaptureElement(JSPECCapture):
    SERIALIZER = lambda element: '(%s)' % str(element)
    ELLIPSIS   = "..."

class JSPECObjectCaptureKey(JSPECCapture):
    SERIALIZER = lambda element: '(%s' % str(element)
    ELLIPSIS   = ""

class JSPECObjectCaptureValue(JSPECCapture):
    SERIALIZER = lambda element: '%s)' % str(element)
    ELLIPSIS   = "..."