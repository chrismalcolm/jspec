"""This module contains the components required to construct a JSPEC instance.
A JSPEC instance consists of a JSPEC entities and every JSPEC entity has it's
own dedicated class. This module defines the JSPEC class and all of the JSPEC
entity classes
"""

#TODO finish documentation


class JSPEC:
    """This class represents a JSPEC.

    A JSPEC instance consists of an arrangement of JSPEC entities. This
    arrangement is derivied from a base JSPEC element.
    
    This JSPEC class must have functionality for the following:
    - Ability to serialize itself as a string (__str__)
    - Ability to know if it is equivalent to another JSPEC (__eq__)

    Attributes:
        term (JSPECTerm): The base JSPEC term for this JSPEC.
        macros (dict): The mapping of macro names to their JSON Python native
            values

    Args:
        element (JSPECTerm): The element to set as the base level JSPEC 
            element for this JSPEC.
    """
    def __init__(self, term, macros=None):
        self.term = term
        self.macros = macros or dict()

    def __str__(self):
        return str(self.term)

    def __eq__(self, other):
        return self.term == other.term


"""
*-----------------------------------------------------------------------------*
JSPEC Standard Elements:

These standard classes correspond with the basic data types for JSON elements.
*-----------------------------------------------------------------------------*
"""

class JSPECEntity:
    
    def __init__(self):
        self.string = ""

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

class JSPECTerm(JSPECEntity):
    """This class represents a JSPEC element.
    
    A JSPEC element is a JSPEC entity that can be used to compare against a
    single JSON element. When a JSPEC element is compared against a JSON
    element, whether the JSON element is a good match or a bad match should be
    able to be determined. Generally JSON element is a good match if it is
    equivalent to the JSPEC Element's ``spec``.
    
    This JSPEC element class must have functionality for the following:
    - Ability to create its ``spec`` from a given value (COVERTER)
    - Ability to create its ``string`` from a given value (SERIALIZER)
    - Ability to serialize itself as a string (__str__)
    - Ability to know if it is equivalent to another JSPEC (__eq__)
    - Ability to have its own hash for mappings (__hash__)

    Attributes:
        spec (obj): The Python native JSON element instance to match
            with
        string (string): The serialization of the JSPEC element
        hash (int): The hash of the JSPEC element, required for mappings

    Args:
        value (obj): Python native instance used to generate the
        ``spec`` and the serialization to make ``string``
    """

    COVERTER = lambda x: None
    """func: Convert the ``value`` into the ``spec``.
    """

    SERIALIZER = lambda x: ""
    """func: Convert the ``value`` into the ``string``.
    """
    
    def __init__(self, value):
        self.spec = self._generator(value)
        self.string = self._serializer(value)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.spec == other.spec

    def _generator(self, value):
        return self.__class__.COVERTER(value)

    def _serializer(self, value):
        return self.__class__.SERIALIZER(value)

class JSPECObjectPair(JSPECEntity):
    """This class represents a JSPEC object key-value pair.
    
    A JSPEC object key-value pair is two JSPEC entities, the key is a JSPEC
    string and the value is a JSPEC element.
    
    This JSPEC element pair class must have functionality for the following:
    - Ability to create its ``spec`` from a given value (COVERTER)
    - Ability to create its ``string`` from a given value (SERIALIZER)
    - Ability to serialize itself as a string (__str__)
    - Ability to know if it is equivalent to another JSPEC (__eq__)
    - Ability to have its own hash for mappings (__hash__)

    Attributes:
        spec (obj): The Python native JSON element instance to match
            with
        string (string): The serialization of the JSPEC element
        hash (int): The hash of the JSPEC element, required for mappings

    Args:
        value (obj): Python native instance used to generate the
        ``spec`` and the serialization to make ``string``
    """

    COVERTER = lambda x: x
    """func: Convert the ``value`` into the ``spec``.
    """

    SERIALIZER = lambda x: str(x[0]) + ": " + str(x[1])
    """func: Convert the ``value`` into the ``string``.
    """
    
    def __init__(self, value):
        self.spec = self._generator(value)
        self.string = self._serializer(value)

    def __hash__(self):
        return self.string.__hash__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.spec == other.spec

    def _generator(self, value):
        return self.__class__.COVERTER(value)

    def _serializer(self, value):
        return self.__class__.SERIALIZER(value)

    def key(self):
        return self.spec[0]

    def value(self):
        return self.spec[1]

class JSPECObject(JSPECTerm):
    """This class represents a JSPEC object.

    Args:
        value (set): set of the form:
            pairs = {
                pair_1,
                pair_2,
                ...
                pair_n
            }
            where each pair_n is a JSPECObjectPair or a
            JSPECObjectCaptureGroup.
    """

    COVERTER = lambda pairs: pairs
    """func: Identity on pairs.
    """

    SERIALIZER = lambda pairs: '{%s}' % ', '.join([str(pair) for pair in pairs])
    """func: Serialize ``pairs`` into a comma separated list, enclosed by curly
    parentheses.
    """

    def satisfied_captures(self):
        return (
            all(isinstance(spec, JSPECCapture) for spec in self.spec)
            and all(capture.satisfied() for capture in self.spec)
        )

    def exhausted_captures(self):
        return (
            all(isinstance(spec, JSPECCapture) for spec in self.spec)
            and all(capture.exhausted() for capture in self.spec)
        )

class JSPECObjectPair(JSPECObjectPair):
    """This class represents a JSPEC object pair.

    Args:
        values (tuple): tuple of the form:
            pair = (
                key,
                value,
            )
            where key is a JSPECString and value is a JSPECTerm.
    """

    COVERTER = lambda pair: pair
    """func: Identity on pair.
    """

    SERIALIZER = lambda pair: "%s: %s" % pair
    """func: Serialize ``pair`` as a key-value string.
    """

class JSPECArray(JSPECTerm):
    """This class represents a JSPEC array.

    Args:
        value (list): List of form:
            values = [
                value_1,
                value_2,
                ...
            ]
            where each value_x is a JSPECTerm or a JSPECArrayCaptureGroup.
    """

    COVERTER = list
    """func: Convert values into a Python list.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

    def satisfied_captures(self):
        return (
            all(isinstance(spec, JSPECCapture) for spec in self.spec)
            and all(capture.satisfied() for capture in self.spec)
        )

    def exhausted_captures(self):
        return (
            all(isinstance(spec, JSPECCapture) for spec in self.spec)
            and all(capture.exhausted() for capture in self.spec)
        )

class JSPECString(JSPECTerm):
    """This class represents a JSPEC string.

    Args:
        value (string): A regex string to be matched.
    """

    COVERTER = str
    """func: Convert the value into a Python string.
    """

    SERIALIZER = lambda val: '"%s"' % val
    """func: Serialize ``value`` by applying str and enclosing in double quotes.
    """

class JSPECInt(JSPECTerm):
    """This class represents a JSPEC int.
    
    Args:
        value (int): An integer.
    """

    COVERTER = int
    """func: Convert the value into a Python int.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

class JSPECReal(JSPECTerm):
    """This class represents a JSPEC real.
    
    Args:
        value (float): A real.
    """

    COVERTER = float
    """func: Convert the value into a Python float.
    """

    SERIALIZER = str
    """func: Serialize ``value`` by applying str.
    """

class JSPECBoolean(JSPECTerm):
    """This class represents a JSPEC boolean.

    Args:
        value (bool): A boolean.
    """

    COVERTER = bool
    """func: Convert the value into a Python bool.
    """

    SERIALIZER = lambda val: "true" if bool(val) else "false"
    """func: Returns either 'true' or 'false'.
    """

class JSPECNull(JSPECTerm):
    """This class represents a JSPEC null.

    Args:
        value (None): None.
    """

    COVERTER = lambda val: None
    """func: Convert the value into a Python None.
    """

    SERIALIZER = lambda val: "null"
    """func: Returns 'null'.
    """

class JSPECWildcard(JSPECTerm):
    """This class represents a JSPEC wildcard.

    Args:
        value (None): None.
    """

    COVERTER = lambda val: None
    """func: Returns None.
    """

    SERIALIZER = lambda val: "*"
    """func: Returns '*'.
    """

    def __init__(self):
        super().__init__(None)

class JSPECNegation(JSPECTerm):
    """This class represents a JSPEC negation.

    Args:
        value (JSPECTerm): The JSPEC element to negate.
    """

    COVERTER = lambda val: val
    """func: Returns the value.
    """

    SERIALIZER = lambda val: "!" + str(val)
    """func: Returns the value preceded by a exclamation mark.
    """

class JSPECConditional(JSPECTerm):
    """This class represents a JSPEC conditional.

    Args:
        value (list): A list of alternating instances of the form:
            entities = [
                element_1,
                operator_1,
                element_2,
                operator_2,
                ...
                element_n-1,
                operator_n-1,
                element_n,
            ]
        where each element_x is a JSPECTerm, each operator_y is a
        JSPECLogicalOperator.
    """

    COVERTER = lambda entities: entities
    """func: Returns the entities.
    """

    SERIALIZER = lambda entities: "(" + " ".join(str(e) for e in entities) + ")"
    """func: Returns the entities and operators alternating.
    """

class JSPECMacro(JSPECTerm):
    """This class represents a JSPEC macro.

    Args:
        eval_string (string): String of macro variable.
    """

    COVERTER = lambda eval_string: eval_string
    """func: Returns the eval_string.
    """

    SERIALIZER = lambda eval_string: "<%s>" % eval_string
    """func: Returns the macro variable string enclosed in angled parentheses.
    """

"""
*-----------------------------------------------------------------------------*
JSPEC Placeholders:

This classes represent a placeholder for their given type. It will be a good
match with any JSON element provided it is the matching datatype.
*-----------------------------------------------------------------------------*
"""

class JSPECObjectPlaceholder(JSPECObject):
    """This class represents a JSPEC object placeholder. Matches any object.
    """

    SERIALIZER = lambda _: "object"
    """func: Function which returns the placeholder string for JSPEC objects.
    """

    def __init__(self):
        super().__init__(set())

class JSPECArrayPlaceholder(JSPECArray):
    """This class represents a JSPEC array placeholder. Matches any array.
    """

    SERIALIZER = lambda _: "array"
    """func: Function which returns the placeholder string for JSPEC arrays.
    """

    def __init__(self):
        super().__init__(list())

class JSPECStringPlaceholder(JSPECString):
    """This class represents a JSPEC string placeholder. Matches any string.
    """

    SERIALIZER = lambda _: "string"
    """func: Function which returns the placeholder string for JSPEC strings.
    """

    def __init__(self):
        super().__init__("")

class JSPECBooleanPlaceholder(JSPECBoolean):
    """This class represents a JSPEC boolean placeholder. Matches any
    boolean.
    """

    SERIALIZER = lambda _: "boolean"
    """func: Function which returns the placeholder string for JSPEC boolean.
    """

    def __init__(self):
        super().__init__(False)

class JSPECIntPlaceholder(JSPECInt):
    """This class represents a JSPEC int placeholder. Matches an int that
    satisfies a given basic inequality, or any int.

    Args:
        value (tuple/None): Tuple of the form:
            entities = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda entities: entities
    """func: Returns the entities.
    """

    SERIALIZER = lambda entities: "int" if entities is None else (
        "int %s %s" % (str(entities[0]), str(entities[1]))
    )
    """func: Function which converts the symbol and value into a serialized
    string for an int inequality.
    """

class JSPECRealPlaceholder(JSPECReal):
    """This class represents a JSPEC real placeholder. Matches any real that
    satisfies a given basic inequality, or any real.

    Args:
        value (tuple/None): Tuple of the form:
            entities = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda entities: entities
    """func: Returns the entities.
    """

    SERIALIZER = lambda entities: "real" if entities is None else (
        "real %s %s" % (str(entities[0]), str(entities[1]))
    )
    """func: Function which converts the symbol and value into a serialized
    string for an real inequality.
    """

class JSPECNumberPlaceholder(JSPECConditional):
    """This class represents a JSPEC number placeholder. Matches ant int or
    real that satisfies a given basic inequality, or any int or real.

    Args:
        value (tuple/None): Tuple of the form:
            entities = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda entities: entities
    """func: Returns the entities.
    """

    SERIALIZER = lambda entities: "number" if entities is None else (
        "number %s %s" % (str(entities[0]), str(entities[1]))
    )
    """func: Function which converts the symbol and value into a serialized
    string for an number inequality.
    """

class JSPECInequality(JSPECEntity):
    """This class is the base class that represents a JSPEC inequality.
    """
    
    SYMBOL = ""
    """string: Symbol to represent the inequality symbol. 
    """

    def __init__(self):
        self.string = self.__class__.SYMBOL

    def __eq__(self, other):
        return self.__class__ == other.__class__

class JSPECInequalityLessThan(JSPECInequality):
    """This class is the base class that represents a JSPEC less than
    inequality.
    """
    
    SYMBOL = "<"
    """string: Symbol to represent the less than inequality symbol. 
    """

class JSPECInequalityLessThanOrEqualTo(JSPECInequality):
    """This class is the base class that represents a JSPEC less than or equal
    to inequality.
    """
    
    SYMBOL = "<="
    """string: Symbol to represent the less than or equal to inequality symbol. 
    """

class JSPECInequalityMoreThan(JSPECInequality):
    """This class is the base class that represents a JSPEC more than
    inequality.
    """
    
    SYMBOL = ">"
    """string: Symbol to represent the more than inequality symbol. 
    """

class JSPECInequalityMoreThanOrEqualTo(JSPECInequality):
    """This class is the base class that represents a JSPEC less more or equal
    to inequality.
    """
    
    SYMBOL = ">="
    """string: Symbol to represent the more than or equal to inequality symbol. 
    """

"""
*-----------------------------------------------------------------------------*
JSPEC Logical Operators:

This classes are for the logical operators entities used in JSPEC.
*-----------------------------------------------------------------------------*
"""

class JSPECLogicalOperator(JSPECEntity):
    """This class is the base class that represents a JSPEC logical operator.
    A JSPEC conditional operator is any logical operator that can be used to
    construct logical statements.

    This JSPEC element class must have functionality for the following:
    - Ability to know its symbol to create its ``string`` (SYMBOL)
    - Ability to serialize itself as a string (__str__)
    - Ability to know if it is equivalent to another JSPEC (__eq__)

    Attributes:
        string (string): The serialization of the logical operator
    """

    SYMBOL = ""
    """string: Symbol to represent the logical operation. 
    """

    def __init__(self):
        self.string = self.__class__.SYMBOL

    def __eq__(self, other):
        return self.__class__ == other.__class__

class JSPECLogicalOperatorAnd(JSPECLogicalOperator):
    """This class represents a JSPEC AND logical operator.
    """

    SYMBOL = "&"
    """string: Symbol for AND operation.
    """

class JSPECLogicalOperatorOr(JSPECLogicalOperator):
    """This class represents a JSPEC OR logical operator.
    """

    SYMBOL = "|"
    """string: Symbol for OR operation.
    """

class JSPECLogicalOperatorXor(JSPECLogicalOperator):
    """This class represents a JSPEC XOR logical operator.
    """

    SYMBOL = "^"
    """string: Symbol for XOR operation.
    """


"""
*-----------------------------------------------------------------------------*
JSPEC Capture:

This classes are for the JSPEC capture entities.
*-----------------------------------------------------------------------------*
"""

class JSPECCapture(JSPECEntity):
    """This class represents a JSPEC capture.
    
    A JSPEC capture is any JSPEC entity that can be used to match a group of
    JSON elements. The capture decides the logic of what Python native JSON
    elements compares to give a good match.

    This JSPEC capture class must have functionality for the following:
    - Ability to create its ``string`` from a given arguments (SERIALIZER)
    - Ability to serialize itself as a string (__str__)
    - Ability to know if it is equivalent to another JSPEC (__eq__)
    - Ability to have its own hash for mappings (__hash__)

    Attributes:
        entities (list): List of JSPEC entities
        multiplier (JSPECCaptureMultiplier): Contains info on the range for the
            number of elements a capture should match with.
        string (string): The serialization of the capture
        hash (int): The hash of the capture
        
    Args:
        entities (list): List of JSPEC entities
        multiplier (int, optional): The number of JSON elements the capture has
            to match to be a valid match. Omit for this capture to except any
            number of elements to be a valid match.
    """

    SERIALIZER = lambda entities, multiplier: ""
    """func: Function which converts the entities and multiplier into a
    serialized string
    """

    def __init__(self, entities, multiplier, string=None):
        self.entities = entities
        self.multiplier = multiplier
        self.string = string or self._serializer(entities, multiplier)

    def __hash__(self):
        return self.string.__hash__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.multiplier != other.multiplier:
            return False
        return self.entities == other.entities

    def _serializer(self, value, multiplier):
        return self.__class__.SERIALIZER(value, multiplier)

    def reduced(self):
        return self.__class__(
            self.entities,
            self.multiplier.reduced(),
            string=self.string,
        )

    def satisfied(self):
        return self.multiplier.satisfied()

    def exhausted(self):
        return self.multiplier.exhausted()

class JSPECCaptureMultiplier(JSPECEntity):
    """This class represents a JSPEC capture multiplier.

    It contains a range for the number of elements a capture should match with.

    Attributes:
        minimum (int/None): The minimum for the range of elements to match
            with. If this is None, this is 0.
        maximum (int/None): The maximum for the range of elements to match
            with. If this is None, this is infinity.
        
    Args:
        minimum (int/None): The minimum for the range of elements to match
            with. If this is None, this is 0.
        maximum (int/None): The maximum for the range of elements to match
            with. If this is None, this is infinity.
        string (string): The serialization of the multiplier.
    """

    def __init__(self, minimum=None, maximum=None):
        self.minimum = minimum
        self.maximum = maximum
        self.string = self._string()

    def _string(self):
        minimum = str(self.minimum) if self.minimum != None else '?'
        maximum = str(self.maximum) if self.maximum != None else '?'
        if minimum == maximum:
            return "x%s" % minimum
        return "x%s-%s" % (minimum, maximum)

    def __eq__(self, other):
        return self.minimum == other.minimum and self.maximum == other.maximum

    def reduced(self):
        return self.__class__(
            max(0, self.minimum - 1) if self.minimum is not None else None,
            max(0, self.maximum - 1) if self.maximum is not None else None,
        )

    def satisfied(self):
        return self.minimum == 0 or self.minimum is None

    def exhausted(self):
        return self.maximum == 0

class JSPECArrayCaptureGroup(JSPECCapture):
    """This class represents a JSPEC capture for arrays.

    Args:
        elements (list): List of the form:
           entities = [
                element_1,
                operator_1,
                element_2,
                operator_2,
                ...
                element_n-1,
                operator_n-1,
                element_n,
            ]
            where each element_x is a JSPECTerm and each operator_y is a
            JSPECLogicalOperator.
    """

    SERIALIZER = lambda entities, multiplier: (
        "(%s)" % " ".join(str(e) for e in entities) + str(multiplier)
    )
    """func: Returns the entities and operators alternating, enclosed in
    round parentheses, with a optional x and multiplier."""

class JSPECObjectCaptureGroup(JSPECCapture):
    """This class represents a JSPEC capture pair for objects.

    Args:
        elements (list): List of the form:
           entities = [
                pair_1,
                operator_1,
                pair_2,
                operator_2,
                ...
                pair_n-1,
                operator_n-1,
                pair_n,
            ]
            where each pair_x is a JSPECObjectPair and each operator_y is a
            JSPECLogicalOperator.
    """

    SERIALIZER = lambda entities, multiplier: (
        "(%s)" % " ".join([str(v) for v in entities]) + str(multiplier)
    )
    """func: Returns the key-value pairs and operators alternating, enclosed in
    round parentheses, with a optional x and multiplier.
    """


class JSPECArrayEllipsis(JSPECArrayCaptureGroup):
    """This class represents a JSPEC array ellipsis.
    """
    
    def __init__(self):
        super().__init__([JSPECWildcard()], JSPECCaptureMultiplier(None, None))

    SERIALIZER = lambda entities, multiplier: '...'
    """func: Returns a 3 dot ellipsis.
    """

    def reduced(self):
        return self.__class__()

    def satisfied(self):
        return True

    def exhausted(self):
        return False

class JSPECObjectEllipsis(JSPECObjectCaptureGroup):
    """This class represents a JSPEC object ellipsis.
    """

    def __init__(self):
        super().__init__([JSPECObjectPair((JSPECStringPlaceholder(), JSPECWildcard()))], JSPECCaptureMultiplier(None, None))

    SERIALIZER = lambda entities, multiplier: '...'
    """func: Returns a 3 dot ellipsis.
    """

    def reduced(self):
        return self.__class__()

    def satisfied(self):
        return True

    def exhausted(self):
        return False