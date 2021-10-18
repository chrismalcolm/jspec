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
    JSPECObjectCaptureValue,
)
from error import JSPECDecodeError

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
    [ \t\n\r]* # any space, tab or carrage return characters""", re.VERBOSE).match

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

        if nextchar == "<":
            pair, idx = scan_object_capture(doc, idx)
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
    if nextchar == '>':
        raise JSPECDecodeError("Empty capture", doc, idx)
    if nextchar != '"':
        raise JSPECDecodeError("Expecting property name enclosed in double quotes in capture", doc, idx) 
    key, idx = scan_string(doc, idx)
    nextchar, idx = skip_any_whitespace(doc, idx)
    if nextchar != ':':
        raise JSPECDecodeError("Expecting ':' delimiter in capture", doc, idx)
    _, idx = skip_any_whitespace(doc, idx + 1)
    try:
        value, idx = scan_once(doc, idx)
    except StopIteration as err:
        raise JSPECDecodeError("Expecting value in capture", doc, err.value) from None
    nextchar, idx = skip_any_whitespace(doc, idx)
    if nextchar != '>':
        raise JSPECDecodeError("Expecting capture termination", doc, idx)
    pair = (JSPECObjectCaptureKey(key), JSPECObjectCaptureValue(value))
    return pair, idx + 1

def scan_array(doc, idx):
    values = []
    nextchar, idx = skip_any_whitespace(doc, idx + 1)

    if nextchar == '':
        raise JSPECDecodeError("Unterminated array", doc, idx)
    if nextchar == ']':
        return JSPECArray(values), idx + 1

    while True:
        
        if nextchar == '<':
            value, idx = scan_array_capture(doc, idx)
        else:
            try:
                value, idx = scan_once(doc, idx)
            except StopIteration as err:
                raise JSPECDecodeError("Expecting value", doc, err.value) from None
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
    if nextchar == '>':
        raise JSPECDecodeError("Empty capture", doc, idx)
    try:
        value, idx = scan_once(doc, idx)
    except StopIteration as err:
        raise JSPECDecodeError("Expecting value in capture", doc, err.value) from None
    nextchar, idx = skip_any_whitespace(doc, idx)
    if nextchar != '>':
        raise JSPECDecodeError("Expecting capture termination", doc, idx)
    return JSPECArrayCaptureElement(value), idx + 1
    
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

    if nextchar == '.' and doc[idx:idx+3] == '...':
        return JSPECWildcard(), idx + 3

    if nextchar == 'n' and doc[idx:idx+4] == 'null':
        return JSPECNull(), idx + 4

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