# TODO explanation on what a jspec is

class JSPEC:
    """This class represents a JSPEC.

    Attributes:
        element (JSPECElement): The base level JSPEC element for this JSPEC.

    Args:
        element (JSPECElement): The element to set as the base level JSPEC 
            element for this JSPEC.
    """
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return str(self.element)

    def __eq__(self, other):
        return self.element == other.element


# TODO explanation on what a element is

class JSPECElement:
    """This class is the base class that represents a JSPEC element.

    Attributes:
        spec (obj): The Python native instance to match with
        string (string): The serialization of the element
        hash (int): The hash of the element
        is_placeholder (bool): Whether the element is a placeholder

    Args:
        value (obj): Python native instance used to generate the ``spec`` and
            the serialization to make ``string``
       is_placeholder (bool): Whether the element is a placeholder
    """

    PLACEHOLDER = ""
    """string: How this element is serialzed if 'is_placeholder' is True.
    """

    SPEC_FUNC = lambda x: None
    """func: Convert the ``value`` into the ``spec``.
    """

    SERIALIZER = lambda x: ""
    """func: Convert the ``value`` into the ``string``.
    """
    
    def __init__(self, value, is_placeholder=False):
        self.spec = self._spec_func(value)
        self.string = self._serializer(value) if not is_placeholder else self.PLACEHOLDER
        self.hash = self.string.__hash__()
        self.is_placeholder = is_placeholder

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.is_placeholder and other.is_placeholder:
            return True
        if self.is_placeholder or other.is_placeholder:
            return False
        return self.spec == other.spec

    def _spec_func(self, value):
        return self.__class__.SPEC_FUNC(value)

    def _serializer(self, value):
        return self.__class__.SERIALIZER(value)

class JSPECObject(JSPECElement):
    """This class represents a JSPEC object.

    Args:
        value (list): list of tuple pairs of the form:
            pairs = [
                (key_1: value_1),
                (key_2: value_2),
                ...
            ]
            where each key_x/value_x is a JSPECString/JSPECElement pair or a
            JSPECObjectCaptureKey/JSPECObjectCaptureValue pair.
    """

    PLACEHOLDER = "object"
    """string: Placeholder JSPECObject instances are serialized as 'object'.
    """

    SPEC_FUNC = dict
    """func: Convert pairs into a Python dict.
    """

    SERIALIZER = lambda pairs: str(dict(pairs))
    """func: Serialize ``value`` by applying dict then str.
    """

class JSPECArray(JSPECElement):
    """This class represents a JSPEC array.

    Args:
        value (list): List of form:
            values = [
                value_1,
                value_2,
                ...
            ]
            where each value_x is a JSPECElement or a
            JSPECObjectCaptureElement.
    """

    PLACEHOLDER = "array"
    """string: Placeholder JSPECArray instances are serialized as 'array'.
    """

    SPEC_FUNC = list
    """func: Convert values into a Python list.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

class JSPECString(JSPECElement):
    """This class represents a JSPEC string.

    Args:
        value (string): A regex string to be matched.
    """

    PLACEHOLDER = "string"
    """string: Placeholder JSPECString instances are serialized as 'string'.
    """

    SPEC_FUNC = str
    """func: Convert the value into a Python string.
    """

    SERIALIZER = lambda val: '"%s"' % val
    """func: Serialize ``value`` by applying str and enclosing in double quotes.
    """

class JSPECInt(JSPECElement):
    """This class represents a JSPEC int.
    
    Args:
        value (int): An integer.
    """

    PLACEHOLDER = "int"
    """string: Placeholder JSPECInt instances are serialized as 'int'.
    """

    SPEC_FUNC = int
    """func: Convert the value into a Python int.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

class JSPECReal(JSPECElement):
    """This class represents a JSPEC real.
    
    Args:
        value (float): A real.
    """

    PLACEHOLDER = "real"
    """string: Placeholder JSPECReal instances are serialized as 'real'.
    """

    SPEC_FUNC = float
    """func: Convert the value into a Python float.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

class JSPECBoolean(JSPECElement):
    """This class represents a JSPEC boolean.

    Args:
        value (bool): A boolean.
    """

    PLACEHOLDER = "bool"
    """string: Placeholder JSPECBoolean instances are serialized as 'bool'.
    """

    SPEC_FUNC = bool
    """func: Convert the value into a Python bool.
    """

    SERIALIZER = lambda val: "true" if bool(val) else "false"
    """func: Returns either 'true' or 'false'.
    """

class JSPECNull(JSPECElement):
    """This class represents a JSPEC null.

    Args:
        value (None): None.
    """

    SPEC_FUNC = lambda val: None
    """func: Convert the value into a Python None.
    """

    SERIALIZER = lambda val: "null"
    """func: Returns 'null'.
    """

class JSPECWildcard(JSPECElement):
    """This class represents a JSPEC wildcard.

    Args:
        value (None): None.
    """

    SPEC_FUNC = lambda val: None
    """func: Returns None.
    """

    SERIALIZER = lambda val: "*"
    """func: Returns '*'.
    """

class JSPECConditional(JSPECElement):
    """This class represents a JSPEC conditional.

    Args:
        value (set): Set of the form:
            elements = {
                element_1,
                element_2,
                ...
            }
            where each element_x is a JSPECElement.
    """
    
    SPEC_FUNC = lambda elements: elements
    """func: Returns 'elements'.
    """
    
    SERIALIZER = lambda elements: '(%s)' % (
        " | ".join(sorted([str(element) for element in elements]))
    )
    """func: Returns the elements separated by '|' enclosed in round
    parentheses.
    """


# TODO explanation on what a capture is

class JSPECCapture:
    """This class is the base class that represents a JSPEC capture.

    Attributes:
        elements (list): List of JSPECElement instances
        multiplier (int): The number of elements the capture has to
            match to be a valid match
        string (string): The serialization of the capture
        hash (int): The hash of the capture
        
    Args:
        elements (list): List of JSPECElement instances
        multiplier (int, optional): The number of elements the capture has to
            match to be a valid match. Omit for this capture to except any
            number of elements to be a valid match.
        is_ellipsis (bool, optional): Whether this capture should automatically
            be an ellipsis (a wildcard capture) or not.
    """

    SERIALIZER = lambda elements, multiplier: ""
    """func: Function which converts the elements and multiplier into a
    serialized string
    """

    ELLIPSIS = ""
    """string: How this capture is serialzed if 'is_ellipsis' is True.
    """

    def __init__(self, elements, multiplier=-1, is_ellipsis=False):
        self.elements = elements
        self.multiplier = multiplier
        serialized = self._serializer(elements, multiplier)
        self.string = serialized if not is_ellipsis else self.ELLIPSIS
        self.hash = serialized.__hash__()   

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.multiplier != other.multiplier:
            return False
        return self.elements == other.elements

    def _serializer(self, value, multiplier):
        return self.__class__.SERIALIZER(value, multiplier)

    # TODO this should be removed, splitting should happen in 'matcher'
    #def split(self):
    #    for element in self.elements:
    #        yield self.__class__(
    #            set(element),
    #            self.multiplier,
    #            self.is_ellipsis,
    #        )

class JSPECArrayCaptureElement(JSPECCapture):
    """This class represents a JSPEC capture for arrays.

    Args:
        elements (list): List of the form:
            elements = [
                element_1,
                element_2,
                ...
            ]
            where each element_x is a JSPECElement.
    """
    
    SERIALIZER = lambda elements, multiplier: '<%s>' % (
        " | ".join(sorted([str(element) for element in elements])) +
        ("x%i" % multiplier if multiplier > 0 else "")
    )
    """func: returns the elements separated by '|' enclosed in angled
    parentheses, with a optional x and multiplier."""

    ELLIPSIS = "..."
    """string: a 3 dot ellipsis '...'."""

class JSPECObjectCaptureKey(JSPECCapture):
    """This class represents a JSPEC capture for object keys.

    Args:
        elements (list): List of the form:
            elements = [
                element_1,
                element_2,
                ...
            ]
            where each element_x is a JSPECElement.
    """

    SERIALIZER = lambda elements, multiplier: '<%s' % (
        " | ".join(sorted([str(element) for element in elements]))
    )
    """func: returns the elements separated by '|' preceded by an angled
    parenthesis."""

    ELLIPSIS = ""
    """string: is empty as the full ellipsis string will be serialized by the
    accompanying JSPECObjectCaptureValue."""

class JSPECObjectCaptureValue(JSPECCapture):
    """This class represents a JSPEC capture for object values.

    Args:
        elements (list): List of the form:
            elements = [
                element_1,
                element_2,
                ...
            ]
            where each element_x is a JSPECElement.
    """

    SERIALIZER = lambda elements, multiplier: '%s>' % (
        " | ".join(sorted([str(element) for element in elements])) +
        ("x%i" % multiplier if multiplier > 0 else "")
    )
    """func: returns the elements separated by '|' terminated by an angled
    parenthesis, with a optional x and multiplier.
    """
    
    ELLIPSIS = "\b\b..."
    """string: is two backspaces followed by a 3 dot ellipsis. The two
    backspaces are present to remove the delimiter character between the
    key-value pair in an object serialization. This ensures that the
    JSPECObjectCaptureKey and JSPECObjectCaptureValue pair appear as a '...'.
    """