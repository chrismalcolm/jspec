"""This module defines the JSPEC class the JSPEC entity classes.
"""

class JSPEC:
    """This class represents a JSPEC.

    A JSPEC (Json SPECification) is a tool that can used to check the elements
    and structure of a JSON. It consists of an arrangement of JSPEC entities,
    which define a specification for a JSON. Any JSON that meets the
    specification is called a good match and is said to 'match' the JSPEC.
    Any JSON which does not meet the specification is called a bad match and is
    said to 'not match' the JSPEC. The same terminology extends to matching
    with JSPEC entities too.
    
    The arrangement of JSPEC entities is derived from a base JSPEC term.

    A JSON element will match with an instance of this class, provided it
    matches with the base JSPEC term.

    Attributes:
        base (JSPECTerm): The base JSPEC term for this JSPEC.

    Args:
        term (JSPECTerm): The term to set as the base JSPEC term for this
            JSPEC.
    """

    def __init__(self, term):
        self.base = term

    def __str__(self):
        return str(self.base)

    def __eq__(self, other):
        return self.base == other.base

class JSPECEntity:
    """This class represents a JSPEC entity.

    This class is the base class for anything that can be used in a JSPEC.

    The documentation for each JSPEC entity should define what is it, and how
    in can match with element(s) in a JSON.

    Attributes:
        string (str): The serialization of the JSPEC entity
    """

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

class JSPECTerm(JSPECEntity):
    """This class represents a JSPEC term.
    
    A JSPEC term is any JSPEC entity that can be used to compare against a
    single JSON element.
    
    This class is the base class for any JSPEC terms.

    A JSON element will match with a JSPEC term of the appropriate type,
    provided it satisfies ``self.spec``. How a JSON element can satisfy
    ``self.spec`` depends on the particular JSPEC term.

    Attributes:
        spec (obj): A Python native object, used to determine if a JSON
            element matches the JSPEC term
        string (str): The serialization of the JSPEC entity

    Args:
        value (obj): Python native object used to be converted to create
        ``self.spec`` and the serialization to make ``self.string``
    """

    COVERTER = lambda x: None
    """func: Convert the ``value`` into ``self.spec``.
    """

    SERIALIZER = lambda x: ""
    """func: Convert the ``value`` into ``self.string``.
    """
    
    def __init__(self, value):
        self.spec = self._converter(value)
        self.string = self._serializer(value)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.spec == other.spec

    def _converter(self, value):
        return self.__class__.COVERTER(value)

    def _serializer(self, value):
        return self.__class__.SERIALIZER(value)

class JSPECObject(JSPECTerm):
    """This class represents a JSPEC object.

    A JSPEC object is a set of JSPEC object pairs and JSPEC object captures.

    A JSON object will match with an instance of this class, provided it can
    match all the JSPEC object pairs and satisfy all JSPEC object captures.

    Args:
        value (set): set of the form:
            pairs = {
                pair_1,
                pair_2,
                ...
                pair_n
            }
            where each pair_n is a ``JSPECObjectPair`` or a
            ``JSPECObjectCaptureGroup``.
    """

    COVERTER = lambda pairs: pairs
    """func: Convert the ``pairs`` into ``self.spec``.
    """

    SERIALIZER = lambda pairs: '{%s}' % ', '.join(sorted([str(pair) for pair in pairs]))
    """func: Serialize the ``pairs`` into a comma separated list, enclosed by
    curly parentheses.
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

class JSPECObjectPair(JSPECEntity):
    """This class represents a JSPEC object key-value pair.
    
    A JSPEC object key-value pair is two JSPEC terms, the key is a JSPEC string
    and the value is a JSPEC term.
    
    A JSON object key-value pair will match with an instance of this class,
    provided it matches with the corresponding key and value JSPEC terms.

    Attributes:
        spec (tuple): A tuple of the form:
            pair = (
                key,
                value
            )
            where key is a ``JSPECString`` and value is a ``JSPECTerm``.
        string (string): The serialization of the JSPEC element

    Args:
        value (tuple): A tuple of the form:
            pair = (
                key,
                value
            )
            where key is a ``JSPECString`` and value is a ``JSPECTerm``.
    """

    COVERTER = lambda pair: pair
    """func: Convert the ``pair`` into ``self.spec``.
    """

    SERIALIZER = lambda pair: "%s: %s" % pair
    """func: Serialize the ``pair`` into the the key and value serializations,
    separated by a colon and a single space.
    """
    
    def __init__(self, value):
        self.spec = self._converter(value)
        self.string = self._serializer(value)

    def __hash__(self):
        return self.string.__hash__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.spec == other.spec

    def _converter(self, value):
        return self.__class__.COVERTER(value)

    def _serializer(self, value):
        return self.__class__.SERIALIZER(value)

    def key(self):
        return self.spec[0]

    def value(self):
        return self.spec[1]

class JSPECArray(JSPECTerm):
    """This class represents a JSPEC array.

    A JSPEC array is a list of JSPEC terms and array captures.

    A JSON array will match an with instance of this class, provided it can
    match all the JSPEC terms and satisfy all JSPEC array captures.

    Args:
        value (list): List of form:
            values = [
                value_1,
                value_2,
                ...
            ]
            where each value_x is a ``JSPECTerm`` or a
            ``JSPECArrayCaptureGroup``.
    """

    COVERTER = list
    """func: Convert the ``values`` into a Python list.
    """

    SERIALIZER = str
    """func: Serialize the ``values`` by applying str.
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

    A JSPEC string is a regex pattern string.

    A JSON string will match an instance of this class, provided it satisfies
    the regex pattern string. 

    Args:
        value (string): A regex pattern string.
    """

    COVERTER = str
    """func: Convert the ``value`` into a Python string.
    """

    SERIALIZER = lambda value: '"%s"' % value
    """func: Serialize the ``value`` by applying str and enclosing in double
    quotes.
    """

class JSPECInt(JSPECTerm):
    """This class represents a JSPEC int.

    A JSPEC int is an integer.

    A JSON int will match an with an instance of this class, provided its
    integer value equals the integer value of the JSPEC int.
    
    Args:
        value (int): An integer.
    """

    COVERTER = int
    """func: Convert the ``value`` into a Python int.
    """

    SERIALIZER = str
    """func: Serialize the ``value`` by applying str.
    """

class JSPECReal(JSPECTerm):
    """This class represents a JSPEC real.

    A JSPEC real is a real number.

    A JSON real will match an with an instance of this class, provided its real
    number value equals the real number value of the JSPEC real.
    
    Args:
        value (float): A real.
    """

    COVERTER = float
    """func: Convert the value into a Python float.
    """

    SERIALIZER = str
    """func: Serialize the ``value`` by applying str.
    """

class JSPECBoolean(JSPECTerm):
    """This class represents a JSPEC boolean.

    A JSPEC boolean is a boolean.

    A JSON boolean will match an with an instance of this class, provided its
    boolean value equals the boolean value of the JSPEC boolean.

    Args:
        value (bool): A boolean.
    """

    COVERTER = bool
    """func: Convert the ``value`` into a Python bool.
    """

    SERIALIZER = lambda val: "true" if bool(val) else "false"
    """func: Serialize the ``value`` as either 'true' or 'false'.
    """

class JSPECNull(JSPECTerm):
    """This class represents a JSPEC null.

    A JSPEC null is a null.

    A JSON null value will match with an instance of this class.

    Args:
        value (None): None.
    """

    COVERTER = lambda val: None
    """func: Convert the ``value`` into a Python None.
    """

    SERIALIZER = lambda val: "null"
    """func: Serialize the ``value`` as 'null'.
    """

class JSPECWildcard(JSPECTerm):
    """This class represents a JSPEC wildcard.

    A JSPEC wildcard is the JSPEC term that will match with any JSON element.

    Args:
        value (None): None.
    """

    COVERTER = lambda _: None
    """func: Returns Python None.
    """

    SERIALIZER = lambda _: "*"
    """func: Returns '*'.
    """

    def __init__(self):
        super().__init__(None)

class JSPECNegation(JSPECTerm):
    """This class represents a JSPEC negation.

    A JSPEC negation is a negated JSPEC term.

    A JSON element will match with an element of this class, provided it does 
    not match with the negated JSPEC term.

    Args:
        value (JSPECTerm): The negated JSPEC term.
    """

    COVERTER = lambda term: term
    """func: Convert the ``term`` as``self.spec``.
    """

    SERIALIZER = lambda term: "!%s" % term
    """func: Serialize the ``term`` as its serialization, preceded by an
    exclamation mark.
    """

class JSPECMacro(JSPECTerm):
    """This class represents a JSPEC macro.

    A JSPEC macro is a variable name which can be exported as a Python native
    JSON constant during the matching process. These variables are environment
    variables.
    
    A JSON element will match with an instance of this class, provided that it
    equals the exported Python native JSON constant.

    Args:
        eval_string (string): String of macro variable name.
    """

    COVERTER = str
    """func: Converts the ``name`` into a Python string.
    """

    SERIALIZER = lambda name: "<%s>" % name
    """func: Returns the macro variable name, enclosed in angled parentheses.
    """

class JSPECConditional(JSPECTerm):
    """This class represents a JSPEC conditional.

    A JSPEC conditional is a list of JSPEC terms, with each JSPEC term
    separated by JSPEC logical operator. This forms a logical statement of
    JSPEC terms and JSPEC logical operators.

    A JSON element will match with an instance of this class, provided it
    satisfies the logical statement of JSPEC terms and JSPEC logical operators.

    Args:
        value (list): A list of alternating instances of the form:
            entities = [
                term_1,
                operator_1,
                term_2,
                operator_2,
                ...
                term_n-1,
                operator_n-1,
                term_n,
            ]
        where each term_x is a JSPECTerm, each operator_y is a
        JSPECLogicalOperator.
    """

    COVERTER = list
    """func: Converts the ``entities`` into a Python list.
    """

    SERIALIZER = lambda entities: "(" + " ".join(str(e) for e in entities) + ")"
    """func: Serialize the entities and operators as a string, with the
    serializations of the entities, separated by a single space enclosed in
    rounded parentheses.
    """

class JSPECLogicalOperator(JSPECEntity):
    """This class is the base class that represents a JSPEC logical operator.
    
    A JSPEC logical operator is any logical operator that can be used to
    construct logical statements.

    Attributes:
        string (str): The serialization of the logical operator
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

class JSPECObjectPlaceholder(JSPECObject):
    """This class represents a JSPEC object placeholder.
    
    A JSON element will match with an instance of this class, provided it is an
    object.
    """

    SERIALIZER = lambda _: "object"
    """func: Returns the placeholder string for JSPEC objects.
    """

    def __init__(self):
        super().__init__(set())

class JSPECArrayPlaceholder(JSPECArray):
    """This class represents a JSPEC array placeholder.

    A JSON element will match with an instance of this class, provided it is a
    array.
    """

    SERIALIZER = lambda _: "array"
    """func: Returns the placeholder string for JSPEC arrays.
    """

    def __init__(self):
        super().__init__(list())

class JSPECStringPlaceholder(JSPECString):
    """This class represents a JSPEC string placeholder.

    A JSON element will match with an instance of this class, provided it is a
    string.
    """

    SERIALIZER = lambda _: "string"
    """func: Returns the placeholder string for JSPEC strings.
    """

    def __init__(self):
        super().__init__("")

class JSPECBooleanPlaceholder(JSPECBoolean):
    """This class represents a JSPEC boolean placeholder. 
    
    A JSON element will match with an instance of this class, provided it is a
    boolean.
    """

    SERIALIZER = lambda _: "bool"
    """func: Returns the placeholder string for JSPEC boolean.
    """

    def __init__(self):
        super().__init__(False)

class JSPECIntPlaceholder(JSPECInt):
    """This class represents a JSPEC int placeholder. 
    
    A JSON element will match with an instance of this class, provided it is an
    int, and optionally satisfies the given inequality.

    Args:
        value (tuple/None): Tuple of the form:
            values = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda values: values
    """func: Converts the ``values`` into ``self.spec``.
    """

    SERIALIZER = lambda values: "int" if values is None else (
        "int %s %s" % (str(values[0]), str(values[1]))
    )
    """func: Returns 'int' followed by the optional serialization of the 
    ``values``.
    """

class JSPECRealPlaceholder(JSPECReal):
    """This class represents a JSPEC real placeholder.
    
    A JSON element will match with an instance of this class, provided it is an
    real, and optionally satisfies the given inequality.

    Args:
        value (tuple/None): Tuple of the form:
            values = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda values: values
    """func: Converts the ``values`` into ``self.spec``.
    """

    SERIALIZER = lambda values: "real" if values is None else (
        "real %s %s" % (str(values[0]), str(values[1]))
    )
    """func: Returns 'real' followed by the optional serialization of the 
    ``values``.
    """

class JSPECNumberPlaceholder(JSPECConditional):
    """This class represents a JSPEC number placeholder.

    A JSON element will match with an instance of this class, provided it is an
    int or real, and optionally satisfies the given inequality.

    Args:
        value (tuple/None): Tuple of the form:
            values = (
                symbol,
                value,
            )
            where symbol is a JSPECInequality and value is a number.
            or None for no inequality.
    """

    COVERTER = lambda values: values
    """func: Converts the ``values`` into ``self.spec``.
    """

    SERIALIZER = lambda values: "number" if values is None else (
        "number %s %s" % (str(values[0]), str(values[1]))
    )
    """func: Returns 'number' followed by the optional serialization of the 
    ``values``.
    """

class JSPECInequality(JSPECEntity):
    """This class represents a JSPEC inequality symbol.
    
    This class is the base class that represents a JSPEC inequality symbol.
    """
    
    SYMBOL = ""
    """string: Symbol to represent the inequality symbol. 
    """

    def __init__(self):
        self.string = self.__class__.SYMBOL

    def __eq__(self, other):
        return self.__class__ == other.__class__

class JSPECInequalityLessThan(JSPECInequality):
    """This class represents a JSPEC less than inequality symbol.
    """
    
    SYMBOL = "<"
    """string: Symbol to represent the less than inequality symbol. 
    """

class JSPECInequalityLessThanOrEqualTo(JSPECInequality):
    """This class represents a JSPEC less than or equal to inequality symbol.
    """
    
    SYMBOL = "<="
    """string: Symbol to represent the less than or equal to inequality symbol.
    """

class JSPECInequalityMoreThan(JSPECInequality):
    """This class represents a JSPEC more than inequality symbol.
    """
    
    SYMBOL = ">"
    """string: Symbol to represent the more than inequality symbol. 
    """

class JSPECInequalityMoreThanOrEqualTo(JSPECInequality):
    """This class represents a JSPEC more than or equal to inequality symbol.
    """
    
    SYMBOL = ">="
    """string: Symbol to represent the more than or equal to inequality symbol.
    """

class JSPECCapture(JSPECEntity):
    """This class represents a JSPEC capture.
    
    A JSPEC capture is any JSPEC entity that can be used to match a group of
    JSON elements.
    
    It is a list of JSPEC entities and logical operators which form a logical
    statement. It also has an optional minimum and maximum.
    
    A group of JSON elements will match with an instance of this type, provided
    that each element satisfies the logical statement of JSPEC entities and
    JSPEC logical operators, and the number of JSON elements in the group is
    between the optional minimum and maximum.

    A capture is called 'satisfied' if it has found a group of JSON elements
    which match with it. A capture is called 'exhausted' if the capture can not
    match with any more elements, as it is already filled up.

    Attributes:
        entities (list): List of JSPEC entities
        multiplier (JSPECCaptureMultiplier): Contains info on the range for the
            number of elements a capture should match with.
        string (str): The serialization of the capture
        
    Args:
        entities (list): List of JSPEC entities
        multiplier (int): The number of JSON elements the capture has
            to match to be a valid match. Omit for this capture to except any
            number of elements to be a valid match.
        string (str, optional): The string to set as ``self.string``, if
            omitted, the serialization of the capture
    """

    SERIALIZER = lambda entities, multiplier: ""
    """func: Function which converts the ``entities`` and ``multiplier`` into a
    serialized string.
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

    It contains a range for the number of JSPEC terms a capture needs to match
    in order to be satisfied.

    Attributes:
        minimum (int, optional): The minimum for the range of JSPEC terms a
            capture needs to match. If this is None, this is 0.
        maximum (int, optional): The maximum for the range of JSPEC terms a
            capture needs to match. If this is None, this is infinity.
        
    Args:
        minimum (int, optional): The minimum for the range of JSPEC terms a
            capture needs to match. If this is None, this is 0.
        maximum (int, optional): The maximum for the range of JSPEC terms a
            capture needs to match. If this is None, this is infinity.
        string (str): The serialization of the multiplier.
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

class JSPECObjectCaptureGroup(JSPECCapture):
    """This class represents a JSPEC object capture.

    It is a list of JSPEC object pairs and logical operators which form a
    logical statement. It also has an optional minimum and maximum.
    
    A group of JSON elements will match with an instance of this type, provided
    that each object pair satisfies the logical statement of JSPEC object pairs
    and JSPEC logical operators, and the number of JSON elements in the group is
    between the optional minimum and maximum.

    Args:
        entities (list): List of the form:
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

class JSPECArrayCaptureGroup(JSPECCapture):
    """This class represents a JSPEC array capture.

    It is a list of JSPEC terms and JSPEC logical operators which form a
    logical statement. It also has an optional minimum and maximum.
    
    A group of JSON elements will match with an instance of this type, provided
    that each element satisfies the logical statement of JSPEC terms and JSPEC
    logical operators, and the number of JSON elements in the group is between
    the optional minimum and maximum.

    Args:
        entities (list): List of the form:
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

class JSPECObjectEllipsis(JSPECObjectCaptureGroup):
    """This class represents a JSPEC object ellipsis.
    """

    def __init__(self):
        super().__init__(
            [JSPECObjectPair((JSPECStringPlaceholder(), JSPECWildcard()))],
            JSPECCaptureMultiplier(None, None),
        )

    SERIALIZER = lambda entities, multiplier: '...'
    """func: Returns a 3 dot ellipsis.
    """

    def reduced(self):
        return self.__class__()

    def satisfied(self):
        return True

    def exhausted(self):
        return False

class JSPECArrayEllipsis(JSPECArrayCaptureGroup):
    """This class represents a JSPEC array ellipsis.
    """
    
    def __init__(self):
        super().__init__(
            [JSPECWildcard()], 
            JSPECCaptureMultiplier(None, None),
        )

    SERIALIZER = lambda entities, multiplier: '...'
    """func: Returns a 3 dot ellipsis.
    """

    def reduced(self):
        return self.__class__()

    def satisfied(self):
        return True

    def exhausted(self):
        return False