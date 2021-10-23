import re

from component import (
    JSPEC,
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
    JSPECWildcard,
    JSPECNull,
    JSPECArrayCaptureElement,
    JSPECObjectCaptureKey,
    JSPECObjectCaptureValue
)

STRING_MATCH = re.compile(r"""
    "     # preceded by a double quote
    (.*?) # any character except \n, zero or more times (not greedy)
    "     # terminated by a double quote""", re.VERBOSE).match

NUMBER_MATCH = re.compile(r"""
    (-?(?:0|[1-9]\d*)) # integer, signed digit string with no leading zeroes
    (\.\d+)?           # fractional part, digit string preceded by a decimal point
    ([eE][-+]?\d+)?    # exponent, eE followied by a signed digit string""", re.VERBOSE).match

WHITESPACE_CHARACTERS = ' \t\n\r'
WHITESPACE_MATCH = re.compile(r"""
    [ \t\n\r]* # any space, tab, newline or carrage return characters""", re.VERBOSE).match

MULTIPLIER_MATCH = re.compile(r"""
    x          # preceded by an x
    ([1-9]\d*) # positive integer, unsigned digit string with no leading zeroes """, re.VERBOSE).match

class JSPECDecodeError(ValueError):

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

def skip_any_whitespace(doc, idx):
    nextchar = doc[idx:idx + 1]
    if nextchar not in WHITESPACE_CHARACTERS:
        return nextchar, idx
    idx = WHITESPACE_MATCH(doc, idx).end()
    nextchar = doc[idx:idx + 1]
    return nextchar, idx

def scan_object(doc, idx):
    pairs = []
    nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar == '':
        raise JSPECDecodeError("Unterminated object", doc, idx)
    if nextchar == '}':
        return JSPECObject(pairs), idx + 1

    while True:
        nextchar = doc[idx:idx + 1]

        if nextchar == "(":
            pair, idx = scan_object_capture(doc, idx)
        elif nextchar == '.':
            pair, idx = scan_object_ellipsis(doc, idx)
        else:
            if nextchar != '"':
                raise JSPECDecodeError("Expecting property name enclosed in double quotes", doc, idx) 
            key, idx = scan_string(doc, idx)
            nextchar, idx = skip_any_whitespace(doc, idx)
            if nextchar != ':':
                raise JSPECDecodeError("Expecting ':' delimiter", doc, idx)
            _, idx = skip_any_whitespace(doc, idx + 1)
            try:
                value, idx = scan_once(doc, idx)
            except StopIteration as err:
                raise JSPECDecodeError("Expecting value", doc, err.value) from None
            pair = (key, value)
        if pair[0] in [p[0] for p in pairs]:
            if isinstance(pair[0], JSPECObjectCaptureKey):
                raise JSPECDecodeError("Redundant object capture", doc, idx)
            else:
                raise JSPECDecodeError("Repeated object key", doc, idx)
        pairs.append(pair)

        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == '}':
            return JSPECObject(pairs), idx + 1
        if nextchar == '':
            raise JSPECDecodeError("Unterminated object", doc, idx)
        if nextchar != ',':
            raise JSPECDecodeError("Expecting ',' delimiter", doc, idx)
        _, idx = skip_any_whitespace(doc, idx + 1)

def scan_object_capture(doc, idx):
    nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar == ')':
        raise JSPECDecodeError("Empty capture", doc, idx)
    keys = set()
    vals = set()
    while True:
        if nextchar != '"':
            raise JSPECDecodeError("Expecting property name enclosed in double quotes in capture", doc, idx) 
        key, idx = scan_string(doc, idx)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar != ':':
            raise JSPECDecodeError("Expecting ':' delimiter in capture", doc, idx)
        _, idx = skip_any_whitespace(doc, idx + 1)
        try:
            val, idx = scan_once(doc, idx)
        except StopIteration as err:
            raise JSPECDecodeError("Expecting value in capture", doc, err.value) from None
        if key in keys:
            raise JSPECDecodeError("Repeated key in conditional", doc, idx)
        keys.add(key)
        vals.add(val)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar != '|':
            break
        nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar != ')':
        raise JSPECDecodeError("Expecting capture termination", doc, idx)
    idx += 1
    m = MULTIPLIER_MATCH(doc, idx)
    if m is None:
        pair = (
            JSPECObjectCaptureKey(keys), 
            JSPECObjectCaptureValue(vals)
        )
        return pair, idx
    multiplier = int(m.groups()[0])
    pair = (
        JSPECObjectCaptureKey(keys, multiplier=multiplier), 
        JSPECObjectCaptureValue(vals, multiplier=multiplier)
    )
    return pair, m.end()

def scan_object_ellipsis(doc, idx):
    if not doc[idx:idx + 3] == '...':
        raise JSPECDecodeError("Expecting ellipsis with 3 dots", doc, idx)
    key_element = JSPECString("", is_placeholder=True)
    val_element = JSPECWildcard(None)
    pair = (
        JSPECObjectCaptureKey(key_element, is_ellipsis=True), 
        JSPECObjectCaptureValue(val_element, is_ellipsis=True)
    )
    return pair, idx + 3

def scan_array(doc, idx):
    values = []
    nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar == '':
        raise JSPECDecodeError("Unterminated array", doc, idx)
    if nextchar == ']':
        return JSPECArray(values), idx + 1

    while True:
        
        if nextchar == '(':
            value, idx = scan_array_capture(doc, idx)
        elif nextchar == '.':
            value, idx = scan_array_ellipsis(doc, idx)
        else:
            try:
                value, idx = scan_once(doc, idx)
            except StopIteration as err:
                raise JSPECDecodeError("Expecting value", doc, err.value) from None
        if len(values) > 0 and isinstance(value, JSPECArrayCaptureElement) and value == values[-1]:
            raise JSPECDecodeError("Redundant array capture", doc, idx)
        values.append(value)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar == ']':
            return JSPECArray(values), idx + 1
        if nextchar == '':
            raise JSPECDecodeError("Unterminated array", doc, idx)
        if nextchar != ',':
            raise JSPECDecodeError("Expecting ',' delimiter", doc, idx)
        nextchar, idx = skip_any_whitespace(doc, idx + 1)

def scan_array_capture(doc, idx):
    nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar == ')':
        raise JSPECDecodeError("Empty capture", doc, idx)
    elements = set()
    while True:
        try:
            element, idx = scan_once(doc, idx)
        except StopIteration as err:
            raise JSPECDecodeError("Expecting value in capture", doc, err.value) from None
        if element in elements:
            raise JSPECDecodeError("Repeated element in conditional", doc, idx)
        elements.add(element)
        nextchar, idx = skip_any_whitespace(doc, idx)
        if nextchar != '|':
            break
        nextchar, idx = skip_any_whitespace(doc, idx + 1)
    if nextchar != ')':
        raise JSPECDecodeError("Expecting capture termination", doc, idx)
    idx += 1
    m = MULTIPLIER_MATCH(doc, idx)
    if m is None:
        return JSPECArrayCaptureElement(elements), idx
    multiplier = int(m.groups()[0])
    return JSPECArrayCaptureElement(elements, multiplier=multiplier), m.end()

def scan_array_ellipsis(doc, idx):
    if not doc[idx:idx + 3] == '...':
        raise JSPECDecodeError("Expecting ellipsis with 3 dots", doc, idx)
    element = JSPECWildcard(None)
    return JSPECArrayCaptureElement(element, is_ellipsis=True), idx + 3

def scan_string(doc, idx):
    m = STRING_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Unterminated string at", doc, idx)
    s, = m.groups()
    value = JSPECString(s)
    return value, m.end()

def scan_number(doc, idx):
    m = NUMBER_MATCH(doc, idx)
    if m is None:
        raise JSPECDecodeError("Invalid number at", doc, idx)
    integer, frac, exp = m.groups()
    if frac is None and exp is None:
        value = JSPECInt(integer)
    else:
        value = JSPECReal(integer + (frac or '') + (exp or ''))
    return value, m.end()

def scan_once(doc, idx):
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

    if nextchar == 't' and doc[idx:idx+4] == 'true':
        return JSPECBoolean(True), idx + 4
    
    if nextchar == 'f' and doc[idx:idx+5] == 'false':
        return JSPECBoolean(False), idx + 5

    if nextchar == 'n' and doc[idx:idx+4] == 'null':
        return JSPECNull(), idx + 4

    if nextchar == '*':
        return JSPECWildcard(), idx + 1

    if nextchar == 'o' and doc[idx:idx+6] == 'object':
        return JSPECObject({}, placeholder=True), idx + 6

    if nextchar == 'a' and doc[idx:idx+5] == 'array':
        return JSPECArray([], placeholder=True), idx + 5

    if nextchar == 's' and doc[idx:idx+6] == 'string':
        return JSPECString("", placeholder=True), idx + 6

    if nextchar == 'i' and doc[idx:idx+3] == 'int':
        return JSPECInt(0, placeholder=True), idx + 3

    if nextchar == 'r' and doc[idx:idx+4] == 'real':
        return JSPECReal(0, placeholder=True), idx + 4

    if nextchar == 'b' and doc[idx:idx+4] == 'bool':
        return JSPECBoolean(False, placeholder=True), idx + 4

    raise StopIteration(idx)

def scan(doc):
    _, start = skip_any_whitespace(doc, 0)
    try:
        element, idx = scan_once(doc, start)
    except StopIteration as err:
        raise JSPECDecodeError("Expecting value", doc, err.value) from None
    _, end = skip_any_whitespace(doc, idx)
    if end != len(doc):
        raise JSPECDecodeError("Extra data", doc, end)
    result = JSPEC(element)
    return result