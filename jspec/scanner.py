"""Module for scanning JSPEC documents.
"""
#TODO finise docs

import re

from .component import (
    JSPEC,
    JSPECObjectPair,
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
    JSPECNull,
    JSPECWildcard,
    JSPECNegation,
    JSPECConditional,
    JSPECObjectPlaceholder,
    JSPECArrayPlaceholder,
    JSPECStringPlaceholder,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECBooleanPlaceholder,
    JSPECNumberPlaceholder,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECArrayCaptureGroup,
    JSPECObjectCaptureGroup,
    JSPECArrayEllipsis,
    JSPECObjectEllipsis,
    JSPECCaptureMultiplier,
)

class JSPECDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:
    
    Args:
        msg (str): The unformatted error message
        doc (str): The JSPEC document being parsed
        pos (int): The start index of doc where parsing failed

    Attributes:
        msg (str): The unformatted error message
        doc (str): The JSPEC document being parsed
        pos (int): The start index of doc where parsing failed
        lineno (int): The line corresponding to pos
        colno (int): The column corresponding to pos
    """

    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        errmsg = '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno

    def __reduce__(self):
        return self.__class__, (self.msg, self.doc, self.pos)

STRING_MATCH = re.compile(r"""
    "     # preceded by a double quote
    (.*?) # any character except \n, zero or more times (not greedy)
    "     # terminated by a double quote""", re.VERBOSE).match
"""_sre.SRE_Pattern: Pattern to match a JSPEC string."""

NUMBER_MATCH = re.compile(r"""
    (-?(?:0|[1-9]\d*)) # integer, signed digit string with no leading zeroes
    (\.\d+)?           # fractional part, digit string preceded by a decimal point
    ([eE][-+]?\d+)?    # exponent, eE followed by a signed digit string""", re.VERBOSE).match
"""_sre.SRE_Pattern: Pattern to match a JSPEC int or real."""

WHITESPACE_CHARACTERS = ' \t\n\r'
"""string: Whitespace characters."""

WHITESPACE_MATCH = re.compile(r"""
    [ \t\n\r]* # any space, tab, newline or carrage return characters""", re.VERBOSE).match
"""_sre.SRE_Pattern: Pattern to match whitespace."""

MULTIPLIER_MATCH = re.compile(r"""
    x                    # preceded by an x
    ([1-9]\d*|\?)        # non-negative integer or ?
    (?:\-([1-9]\d*|\?))? # hyphen followed by a non-negative integer or ?""", re.VERBOSE).match
"""_sre.SRE_Pattern: Pattern to match a capture multiplier."""

def skip_any_whitespace(doc, idx):
    """Iterate through characters in ``doc`` starting from index ``idx`` until
    a non-whitespace character is reached.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the iterator.

    Returns:
        str: The first non-whitespace character, starting at index ``idx``
        int: The index of this character in ``doc``
    """
    nextchar = doc[idx:idx + 1]
    if nextchar not in WHITESPACE_CHARACTERS:
        return nextchar, idx
    idx = WHITESPACE_MATCH(doc, idx).end()
    nextchar = doc[idx:idx + 1]
    return nextchar, idx

def scan_object(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC object.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECObject: The JSPECElement that represents the valid JSPEC object
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC object

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC object.
    """
    pairs = set()
    nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar == '':
        raise JSPECDecodeError("Unterminated object", doc, idx)
    if nextchar == '}':
        return JSPECObject(pairs), idx + 1

    while True:
        nextchar = doc[idx:idx + 1]

        if nextchar == '<':
            pair, idx = scan_object_capture(doc, idx)
            if pair in pairs:
                raise JSPECDecodeError("Redundant object pair capture", doc, idx)
        elif nextchar == '.':
            pair, idx = scan_object_ellipsis(doc, idx)
            if pair in pairs:
                raise JSPECDecodeError("Redundant object ellipsis", doc, idx)
        else:
            if nextchar == 's' and doc[idx:idx+6] == 'string':
                key, idx = JSPECString("", is_placeholder=True), idx + 6
            else:
                if nextchar != '"':
                    raise JSPECDecodeError("Expecting property name enclosed in double quotes as key in object pair", doc, idx) 
                key, idx = scan_string(doc, idx)
            nextchar, idx = skip_any_whitespace(doc, idx)
            if nextchar != ':':
                raise JSPECDecodeError("Expecting key-value delimiter ':' in object", doc, idx)
            _, idx = skip_any_whitespace(doc, idx + 1)
            try:
                value, idx = scan_element(doc, idx)
            except StopIteration as err:
                raise JSPECDecodeError("Expecting element as value in object pair", doc, err.value) from None
            pair = JSPECObjectPair((key, value))
            if key in [pair.key() for pair in pairs if isinstance(pair, JSPECObjectPair)]:
                raise JSPECDecodeError("Repeated object key for pair in object", doc, idx)
        pairs.add(pair)

        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == '}':
            return JSPECObject(pairs), idx + 1
        if nextchar == '':
            raise JSPECDecodeError("Unterminated object", doc, idx)
        if nextchar != ',':
            raise JSPECDecodeError("Expecting object pair delimiter ','", doc, idx)
        _, idx = skip_any_whitespace(doc, idx + 1)

def scan_object_capture(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC object capture.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECObjectCaptureGroup: The JSPECCapture object capture pairs that
            represents the valid JSPEC object capture
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC object capture

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC object capture.
    """
    nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar == '>':
        raise JSPECDecodeError("Empty capture", doc, idx)
    
    entities = list()
    while True:
        if nextchar == 's' and doc[idx:idx+6] == 'string':
            key, idx = JSPECStringPlaceholder(), idx + 6
        else:
            if nextchar != '"':
                raise JSPECDecodeError("Expecting property name enclosed in double quotes as key in object capture pair", doc, idx)
            key, idx = scan_string(doc, idx)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar != ':':
            raise JSPECDecodeError("Expecting key-value delimiter ':' in object capture", doc, idx)
        nextchar, idx = skip_any_whitespace(doc, idx + 1)
        try:
            val, idx = scan_element(doc, idx)
        except StopIteration as err:
            raise JSPECDecodeError("Expecting element as value in object capture pair", doc, err.value) from None
        entities.append(JSPECObjectPair((key, val)))
        nextchar, idx = skip_any_whitespace(doc, idx)

        if nextchar == '&':
            entities.append(JSPECLogicalOperatorAnd())
        elif nextchar == '|':
            entities.append(JSPECLogicalOperatorOr())
        elif nextchar == '^':
            entities.append(JSPECLogicalOperatorXor())
        else:
            break
        nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar != '>':
        raise JSPECDecodeError("Expecting object capture termination '>'", doc, idx) 
    idx += 1
    m = MULTIPLIER_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Expecting object capture multiplier", doc, idx)
    x, y = m.groups()[0], m.groups()[1]
    minimum = int(x) if x != '?' else None
    if y is None:
        maximum = minimum
    else:
        maximum = int(y) if y != '?' else None
    if minimum is not None and maximum is not None and minimum > maximum:
        raise JSPECDecodeError("Minimum for object capture multiplier is larger than the maximum", doc, m.end())
    multiplier = JSPECCaptureMultiplier(minimum, maximum)
    return JSPECObjectCaptureGroup(entities, multiplier), m.end()

def scan_object_ellipsis(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC object ellipsis.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECObjectEllipsis: Represents the valid JSPEC object ellipsis
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC object ellipsis

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC object ellipsis.
    """
    if not doc[idx:idx + 3] == '...':
        raise JSPECDecodeError("Expecting object ellipsis with 3 dots '...'", doc, idx)
    return JSPECObjectEllipsis(), idx + 3

def scan_array(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC array.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECArray: The JSPECElement that represents the valid JSPEC array
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC array

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC array.
    """
    values = []
    nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar == '':
        raise JSPECDecodeError("Unterminated array", doc, idx)
    if nextchar == ']':
        return JSPECArray(values), idx + 1

    while True:
        
        if nextchar == '<':
            value, idx = scan_array_capture(doc, idx)
        elif nextchar == '.':
            value, idx = scan_array_ellipsis(doc, idx)
        else:
            try:
                value, idx = scan_element(doc, idx)
            except StopIteration as err:
                raise JSPECDecodeError("Expecting element in array", doc, err.value) from None
        if len(values) > 0 and isinstance(value, JSPECArrayCaptureGroup) and value == values[-1]:
            raise JSPECDecodeError("Redundant array capture", doc, idx)
        values.append(value)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == ']':
            return JSPECArray(values), idx + 1
        if nextchar == '':
            raise JSPECDecodeError("Unterminated array", doc, idx)
        if nextchar != ',':
            raise JSPECDecodeError("Expecting element in array", doc, idx)
        nextchar, idx = skip_any_whitespace(doc, idx + 1)

def scan_array_capture(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC array capture.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECObjectCaptureElement: The JSPECCapture that represents the valid
            JSPEC array capture
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC array capture

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC array capture.
    """
    nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar == '>':
        raise JSPECDecodeError("Empty array capture", doc, idx)
    entities = list()
    while True:
        try:
            element, idx = scan_element(doc, idx)
        except StopIteration as err:
            raise JSPECDecodeError("Expecting element in array capture", doc, err.value) from None
        entities.append(element)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == '&':
            entities.append(JSPECLogicalOperatorAnd())
        elif nextchar == '|':
            entities.append(JSPECLogicalOperatorOr())
        elif nextchar == '^':
            entities.append(JSPECLogicalOperatorXor())
        else:
            break
        _, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar != '>':
        raise JSPECDecodeError("Expecting array capture termination '>'", doc, idx)
    idx += 1
    m = MULTIPLIER_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Expecting array capture multiplier", doc, idx)
    x, y = m.groups()[0], m.groups()[1]
    minimum = int(x) if x != '?' else None
    if y is None:
        maximum = minimum
    else:
        maximum = int(y) if y != '?' else None
    if minimum is not None and maximum is not None and minimum > maximum:
        raise JSPECDecodeError("Minimum for array capture multiplier is larger than the maximum", doc, m.end())
    multiplier = JSPECCaptureMultiplier(minimum, maximum)
    return JSPECArrayCaptureGroup(entities, multiplier), m.end()

def scan_array_ellipsis(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC array ellipsis.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECArrayEllipsis: Represents the valid JSPEC array ellipsis
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC array ellipsis

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC array ellipsis.
    """
    if not doc[idx:idx + 3] == '...':
        raise JSPECDecodeError("Expecting array ellipsis with 3 dots '...'", doc, idx)
    return JSPECArrayEllipsis(), idx + 3

def scan_string(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC string.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECString: The JSPECElement that represents the valid JSPEC string
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC string

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC string.
    """
    m = STRING_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Unterminated string", doc, idx)
    s, = m.groups()
    value = JSPECString(s)
    return value, m.end()

def scan_number(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC number.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECInt/JSPECReal: The JSPECElement that represents the valid JSPEC
            number (i.e int or real)
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC number

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC number.
    """
    m = NUMBER_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Invalid number", doc, idx)
    integer, frac, exp = m.groups()
    if frac is None and exp is None:
        value = JSPECInt(integer)
    else:
        value = JSPECReal(integer + (frac or '') + (exp or ''))
    return value, m.end()

def scan_negation(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC negation.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECNegation: The JSPECElement that represents the valid JSPEC
            negation
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC negation

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC negation.
    """
    _, idx = skip_any_whitespace(doc, idx + 1)
    try:
        element, idx = scan_element(doc, idx)
    except StopIteration as err:
        raise JSPECDecodeError("Expecting element in negation", doc, err.value) from None
    return JSPECNegation(element), idx

def scan_conditional(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC conditional.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECConditional: The JSPECElement that represents the valid JSPEC
            conditional
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC conditional

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC conditional.
    """
    nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar == ')':
        raise JSPECDecodeError("Empty conditional", doc, idx)
    values = list()
    while True:
        try:
            element, idx = scan_element(doc, idx)
        except StopIteration as err:
            raise JSPECDecodeError("Expecting element in conditional", doc, err.value) from None
        values.append(element)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == '&':
            values.append(JSPECLogicalOperatorAnd())
        elif nextchar == '|':
            values.append(JSPECLogicalOperatorOr())
        elif nextchar == '^':
            values.append(JSPECLogicalOperatorXor())
        else:
            break
        _, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar != ')':
        raise JSPECDecodeError("Expecting conditional termination ')'", doc, idx)
    return JSPECConditional(values), idx + 1

def scan_element(doc, idx):
    """Scan through characters in ``doc`` starting from index ``idx`` until the
    characters scanned represeting a valid JSPEC element.

    Args:
        doc (str): The JSPEC document.
        idx (int): The starting index for the scan.

    Returns:
        JSPECElement: The JSPECElement that represents the valid JSPEC element
        int: The index of the character in ``doc`` after the last character
            from the valid JSPEC element

    Raises:
        StopIteration: Raised if the string scanned cannot represent a
            valid JSPEC element.
    """
    try:
        nextchar = doc[idx]
    except IndexError:
        raise StopIteration(idx) from None

    if nextchar == '{':
        return scan_object(doc, idx)

    if nextchar == '[':
        return scan_array(doc, idx)

    if nextchar == '"':
        return scan_string(doc, idx)

    if nextchar in "-0123456789":
        return scan_number(doc, idx)

    if nextchar == '!':
        return scan_negation(doc, idx)

    if nextchar == '(':
        return scan_conditional(doc, idx)

    if nextchar == 't' and doc[idx:idx+4] == 'true':
        return JSPECBoolean(True), idx + 4
    
    if nextchar == 'f' and doc[idx:idx+5] == 'false':
        return JSPECBoolean(False), idx + 5

    if nextchar == 'n' and doc[idx:idx+4] == 'null':
        return JSPECNull(None), idx + 4

    if nextchar == '*':
        return JSPECWildcard(), idx + 1

    if nextchar == 'o' and doc[idx:idx+6] == 'object':
        return JSPECObjectPlaceholder(), idx + 6

    if nextchar == 'a' and doc[idx:idx+5] == 'array':
        return JSPECArrayPlaceholder(), idx + 5

    if nextchar == 's' and doc[idx:idx+6] == 'string':
        return JSPECStringPlaceholder(), idx + 6

    if nextchar == 'i' and doc[idx:idx+3] == 'int':
        return JSPECIntPlaceholder(), idx + 3

    if nextchar == 'r' and doc[idx:idx+4] == 'real':
        return JSPECRealPlaceholder(), idx + 4

    if nextchar == 'b' and doc[idx:idx+4] == 'bool':
        return JSPECBooleanPlaceholder(), idx + 4

    if nextchar == 'n' and doc[idx:idx+6] == 'number':
        return JSPECNumberPlaceholder(), idx + 6

    raise StopIteration(idx)

def scan(doc):
    """Scan through characters in ``doc``to generate a valid JSPEC instance.

    Args:
        doc (str): The JSPEC document.

    Returns:
        JSPEC: The JSPEC instance that represented in ``doc``.

    Raises:
        JSPECDecodeError: Raised if the string scanned cannot represent a
            valid JSPEC.
    """
    _, start = skip_any_whitespace(doc, 0)
    try:
        element, idx = scan_element(doc, start)
    except StopIteration as err:
        raise JSPECDecodeError("Expecting element", doc, err.value) from None
    _, end = skip_any_whitespace(doc, idx)
    if end != len(doc):
        raise JSPECDecodeError("Extra data", doc, end)
    result = JSPEC(element)
    return result