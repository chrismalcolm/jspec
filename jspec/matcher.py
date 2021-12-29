"""Module for matching JSPECs against JSON.
"""

import json
import os
import re

from .entity import (
    JSPECTerm,
    JSPECObject,
    JSPECObjectPair,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
    JSPECNull,
    JSPECWildcard,
    JSPECNegation,
    JSPECMacro,
    JSPECConditional,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECObjectPlaceholder,
    JSPECArrayPlaceholder,
    JSPECStringPlaceholder,
    JSPECBooleanPlaceholder,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECNumberPlaceholder,
    JSPECInequalityLessThan,
    JSPECInequalityLessThanOrEqualTo,
    JSPECInequalityMoreThan,
    JSPECInequalityMoreThanOrEqualTo,
    JSPECArrayCaptureGroup,
    JSPECObjectCaptureGroup,
)

PYTHON_NATIVE = (
    dict, 
    list, 
    str, 
    int, 
    float, 
    bool,
)

class Result:
    """This class represents the result an a attempted match between a JSPEC
    entity and JSON element(s).

    Attributes:
        res (bool): Whether the result is a good match (``True``) or a bad
            match (``False``)
        loc (str): The location in the JSON where the match failed if it was a
            bad match, otherwise None
        msg (str): The reason the match failed if it was a bad match, otherwise
            None
        capture_metadata (tuple): If the match failed on a JSPEC capture, this
            is a tuple:
            meta = (
                jspec_matches,
                json_matches,
            )
            where jspec_matches is the number of successful JSPEC term matches
            and json_matches is the number of successful JSON element matches.

    Args:
        res (bool): Whether the result is a good match (``True``) or a bad
            match (``False``)
        loc (str, optional): The location in the JSON where the match failed if
            it was a bad match
        msg (str, optional): The reason the match failed if it was a bad match
    """

    def __init__(self, res, loc=None, msg=None):
        self.res = res 
        self.loc = loc or ""
        self.msg = msg or ""
        self.capture_metadata = (-1, -1)

    def __bool__(self):
        return bool(self.res)

    def __eq__(self, other):
        return (
            self.capture_metadata[1] == other.capture_metadata[1]
            and self.capture_metadata[0] == other.capture_metadata[0]
        )

    def __lt__(self, other):
        if self.capture_metadata[1] != other.capture_metadata[1]:
            return self.capture_metadata[1] < other.capture_metadata[1]
        return self.capture_metadata[0] < other.capture_metadata[0]

    def reason(self):
        """Returns the formatted reason as to why the match failed if it was a
        bad match, otherwise an empty string
        """
        if self.res:
            return ""
        return "At location %s - %s" % (self.loc, self.msg)

    def with_capture_metadata(self, term, element):
        """Sets ``self.capture_metadata``"""
        self.capture_metadata = term, element
        return self

def GoodMatch():
    """Returns an instance of ``Result`` as a good match."""
    return Result(True)

def BadMatch(loc, msg):
    """Returns an instance of ``Result`` as a bad match, with the given ``loc``
    and ``msg``."""
    return Result(False, loc, msg)

def match(spec, element):
    """Determine if the JSPEC matches the JSON.

    Args:
        spec (JSPEC): The JSPEC to be checked against
        element (obj): A Python native object representing a JSON

    Returns:
        bool: ``True`` if it was a good match, otherwise ``False``.
        str: Details on why the match failed if it was a bad match, otherwise
            an empty string.
    """
    try:
        result = match_element('$', spec.base, element)
    except ValueError as vle:
        raise vle
    return bool(result), result.reason()

def match_element(loc, term, element):
    """Determine if the JSPEC term matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECTerm): The JSPEC term.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC term matches the JSON element.
    """
    if isinstance(term, JSPECObjectPlaceholder):
        return match_object_placeholder(loc, term, element)

    if isinstance(term, JSPECArrayPlaceholder):
        return match_array_placeholder(loc, term, element)
    
    if isinstance(term, JSPECStringPlaceholder):
        return match_string_placeholder(loc, term, element)

    if isinstance(term, JSPECBooleanPlaceholder):
        return match_boolean_placeholder(loc, term, element)

    if isinstance(term, JSPECIntPlaceholder):
        return match_int_placeholder(loc, term, element)

    if isinstance(term, JSPECRealPlaceholder):
        return match_real_placeholder(loc, term, element)

    if isinstance(term, JSPECNumberPlaceholder):
        return match_number_placeholder(loc, term, element)

    if isinstance(term, JSPECObject):
        return match_object(loc, term, element)
   
    if isinstance(term, JSPECArray):
        return match_array(loc, term, element)
    
    if isinstance(term, JSPECString):
        return match_string(loc, term, element)

    if isinstance(term, JSPECInt):
        return match_int(loc, term, element)

    if isinstance(term, JSPECReal):
        return match_real(loc, term, element)

    if isinstance(term, JSPECBoolean):
        return match_boolean(loc, term, element)

    if isinstance(term, JSPECNull):
        return match_null(loc, term, element)  

    if isinstance(term, JSPECWildcard):
        return match_wildcard(loc, term, element)

    if isinstance(term, JSPECNegation):
        return match_negation(loc, term, element)

    if isinstance(term, JSPECMacro):
        return match_macro(loc, term, element)

    if isinstance(term, JSPECConditional):
        return match_conditional(loc, term, element)

    raise ValueError("JSPEC do not support elements of class %s" % term.__class__)

def match_object(loc, term, element):
    """Determine if the JSPEC object matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECObject): The JSPEC object.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC object matches the JSON element
    """
    if not isinstance(element, dict):
        return BadMatch(loc, "expected an object")
    for spec_pair in term.spec:
        if not isinstance(spec_pair, (JSPECObjectPair, JSPECObjectCaptureGroup)):
            raise ValueError("JSPEC objects do not support object paris of class %s" % spec_pair.__class__)
    return match_object_traverse(loc, term, element, 0, 0)

def match_object_traverse(loc, term, element, term_count, element_count):
    """Traverse through the JSPEC object and JSON object to help determine if
    the JSPEC object matches the JSON object.

    Args:
        loc (str): The current location in the JSON
        term (JSPECObject): The JSPEC object.
        element (dict): The Python native object representing a JSON object
        term_count (int): The number of JSPEC object pairs that have been
            matched
        element_count (int): The number of JSON object pairs that have been
            matched

    Returns:
        Result: The result of whether the JSPEC object matches the JSON object
    """
    spec = term.spec

    if len(element) == 0:
        if term.satisfied_captures():
            return GoodMatch()
        return BadMatch(loc, "exhausted JSON object, failed to match the following JSPEC pairs: [%s]" % ", ".join(sorted([str(p) for p in spec]))).with_capture_metadata(term_count, element_count)

    if term.exhausted_captures():
        return BadMatch(loc, "exhausted JSPEC object, failed to match the following JSON pairs: [%s]" % ", ".join([(json.dumps(k)+": "+json.dumps(v)) for k,v in sorted(element.items())])).with_capture_metadata(term_count, element_count)

    bad_matches = [BadMatch(loc, "empty spec")]
    bad_element_pairs = list()
    for spec_pair in spec:
        for element_pair in element.items():
            if isinstance(spec_pair, JSPECObjectPair):
                result = match_object_pair(loc, spec_pair, element_pair).with_capture_metadata(term_count, element_count)
                if bool(result):
                    new_term = JSPECObject(set(p for p in spec if p != spec_pair))
                    new_element = dict(p for p in element.items() if p != element_pair)
                    return match_object_traverse(loc, new_term, new_element, term_count+1, element_count+1)
                bad_matches.append(result)
                bad_element_pairs.append(element_pair)
                continue
            capture = spec_pair
            if capture.exhausted():
                continue
            reduced_capture, result = match_object_capture_group(loc, capture, element_pair, term_count, element_count)
            if bool(result):
                new_term = JSPECObject(set((p if p != capture else reduced_capture) for p in spec))
                new_element = dict(p for p in element.items() if p != element_pair)
                result = match_object_traverse(loc, new_term, new_element, term_count+1, element_count+1)
                if bool(result):
                    return result
            bad_matches.append(result)
            bad_element_pairs.append(element_pair)

    bad_matches.sort(reverse=True)
    if len(bad_matches) >= 2 and bad_matches[0] == bad_matches[1]:
        return BadMatch(loc, "failed to match the following JSON pairs: [%s]" % ", ".join([(json.dumps(k)+": "+json.dumps(v)) for k,v in sorted(bad_element_pairs)]))
    return bad_matches[0]

def match_object_pair(loc, spec_pair, obj_pair):
    """Determine if the JSPEC object pair matches the JSON object pair.

    Args:
        loc (str): The current location in the JSON
        term (JSPECObjectPair): The JSPEC object pair.
        element (tuple): The Python native object representing a JSON object
            pair

    Returns:
        Result: The result of whether the JSPEC object pair matches the JSON
            object pair
    """
    key_result = match_element(loc, spec_pair.key(), obj_pair[0])
    if not bool(key_result):
        return key_result
    value_result = match_element(loc + "." + obj_pair[0], spec_pair.value(), obj_pair[1])
    if not bool(value_result):
        return value_result
    return GoodMatch()

def match_object_capture_group(loc, capture, element_pair, term_count, element_count):
    """Determine if the given JSON object pair can count towards an object pair
    in the JSPEC object capture.

    Args:
        loc (str): The current location in the JSON
        capture (JSPECObjectCaptureGroup): The JSPEC object capture.
        element_pair (tuple): The Python native object representing a JSON
            object pair
        term_count (int): The number of JSPEC object pairs that have been
            matched
        element_count (int): The number of JSON object pairs that have been
            matched

    Returns:
        JSPECObjectCaptureGroup/None: If the JSON object pair can count towards
            an object pair in the JSPEC object capture, this is the reduced
            object capture, otherwise None
        Result: The result of whether the JSON object pair can count towards an
            object pair in the JSPEC object capture.
    """
    result = match_object_pair(loc, capture.entities[0], element_pair)
    value = bool(result)
    i = 1
    while i < len(capture.entities):
        operator = capture.entities[i]
        spec_pair = capture.entities[i+1]
        i += 2
        result = match_object_pair(loc, spec_pair, element_pair)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return capture.reduced(), GoodMatch()
    return None, BadMatch(loc, "failed object capture, '%s: %s' failed to match '%s'" % (json.dumps(element_pair[0]), json.dumps(element_pair[1]), capture)).with_capture_metadata(term_count, element_count)

def match_array(loc, term, element):
    """Determine if the JSPEC array matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECArray): The JSPEC array.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC array matches the JSON element
    """
    if not isinstance(element, list):
        return BadMatch(loc, "expected an array, got '%s'" % json.dumps(element))
    for spec in term.spec:
        if not isinstance(spec, (JSPECTerm, JSPECArrayCaptureGroup)):
            raise ValueError("JSPEC arrays do not support elements of class %s" % spec.__class__)
    return match_array_traverse(loc, term, element, 0, 0)

def match_array_traverse(loc, term, element, term_idx, element_idx):
    """Traverse through the JSPEC array and JSON array to help determine if the
    JSPEC array matches the JSON array.

    Args:
        loc (str): The current location in the JSON
        term (JSPECArray): The JSPEC array.
        element (list): The Python native object representing a JSON array
        term_idx (int): The current index in JSPEC array that has been matched
            up to
        element_idx (int): The current index in the JSON array that has been
            matched up to

    Returns:
        Result: The result of whether the JSPEC array matches the JSON array
    """
    spec = term.spec

    if len(element) == 0:
        if term.satisfied_captures():
            return GoodMatch()
        return BadMatch(loc, "exhausted JSON array, no JSON element left to match '%s'" % spec[0]).with_capture_metadata(term_idx, element_idx)

    if term.exhausted_captures():
        return BadMatch(loc + "[%s]" % element_idx, "exhausted JSPEC array, no JSPEC term left to match '%s'" % element[0]).with_capture_metadata(term_idx, element_idx)
        

    if isinstance(spec[0], JSPECTerm):
        result = match_element("%s[%s]" % (loc,  element_idx), spec[0], element[0]).with_capture_metadata(term_idx, element_idx)
        if not bool(result):
            return result
        return match_array_traverse(loc, JSPECArray(spec[1:]), element[1:], term_idx+1, element_idx+1)
    
    capture = spec[0]
    
    if capture.exhausted():
        return match_array_traverse(loc, JSPECArray(spec[1:]), element,  term_idx+1, element_idx)
    
    if capture.satisfied():
        best_bad_match = BadMatch(loc, "")
        reduced_capture, result = match_array_capture_group(loc, capture, element[0], term_idx, element_idx)
        if bool(result):
            result = match_array_traverse(loc, JSPECArray(spec[1:]), element[1:], term_idx+1, element_idx+1)
            if bool(result):
                return result
            best_bad_match = result if best_bad_match < result else best_bad_match
            result = match_array_traverse(loc, JSPECArray([reduced_capture] + spec[1:]), element[1:], term_idx, element_idx+1)
            if bool(result):
                return result
            best_bad_match = result if best_bad_match < result else best_bad_match
        result = match_array_traverse(loc, JSPECArray(spec[1:]), element, term_idx+1, element_idx)
        if bool(result):
            return result
        best_bad_match = result if best_bad_match < result else best_bad_match
        return best_bad_match

    reduced_capture, result = match_array_capture_group(loc, capture, element[0], term_idx, element_idx)
    if not bool(result):
        return result
    return match_array_traverse(loc, JSPECArray([reduced_capture] + spec[1:]), element[1:], term_idx, element_idx+1)

def match_array_capture_group(loc, capture, element, term_idx, element_idx):
    """Determine if the given JSON element can count towards an element in the
    JSPEC array capture.

    Args:
        loc (str): The current location in the JSON
        capture (JSPECArrayCaptureGroup): The JSPEC array capture.
        element (obj): The Python native object representing a JSON element
        term_idx (int): The current index in JSPEC array that has been matched
            up to
        element_idx (int): The current index in the JSON array that has been
            matched up to

    Returns:
        JSPECArrayCaptureGroup/None: If the JSON element can count towards an
            element in the JSPEC array capture, this is the reduced array
            capture, otherwise None
        Result: The result of whether the JSON element can count towards an
            element in the JSPEC array capture
    """
    result = match_element(loc, capture.entities[0], element)
    value = bool(result)
    i = 1
    while i < len(capture.entities):
        operator = capture.entities[i]
        spec_element = capture.entities[i+1]
        i += 2
        result = match_element(loc, spec_element, element)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return capture.reduced(), GoodMatch()
    return None, BadMatch(loc, "failed array capture, '%s' failed to match '%s'" % (element, capture)).with_capture_metadata(term_idx, element_idx)

def match_int(loc, term, element):
    """Determine if the JSPEC int matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECInt): The JSPEC int.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC int matches the JSON element
    """
    if not isinstance(element, int):
        return BadMatch(loc, "expected a int, got '%s'" % json.dumps(element))
    if term.spec != element:
        return BadMatch(loc, "expected '%s', got '%s'" % (term.spec, json.dumps(element)))
    return GoodMatch()

def match_real(loc, term, element):
    """Determine if the JSPEC real matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECReal): The JSPEC real.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC real matches the JSON element
    """
    if not isinstance(element, float):
        return BadMatch(loc, "expected a real, got '%s'" % json.dumps(element))
    if term.spec != element:
        return BadMatch(loc, "expected '%s', got '%s'" % (term.spec, json.dumps(element)))
    return GoodMatch()

def match_string(loc, term, element):
    """Determine if the JSPEC string matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECString): The JSPEC string.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC string matches the JSON element
    """
    if not isinstance(element, str):
        return BadMatch(loc, "expected a string, got '%s'" % json.dumps(element))
    if re.compile(r'%s' % term.spec).fullmatch(element) is None:
        return BadMatch(loc, "regex pattern '%s' failed to match '%s'" % (term.spec, json.dumps(element)))
    return GoodMatch()

def match_boolean(loc, term, element):
    """Determine if the JSPEC boolean matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECBoolean): The JSPEC boolean.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC boolean matches the JSON
            element
    """
    if not isinstance(element, bool):
        return BadMatch(loc, "expected a boolean, got '%s'" % json.dumps(element))
    if term.spec != element:
        return BadMatch(loc, "expected '%s', got '%s'" % (term.spec, json.dumps(element)))
    return GoodMatch()

def match_null(loc, term, element):
    """Determine if the JSPEC null matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECNull): The JSPEC null.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC null matches the JSON element
    """
    if element is not None:
        return BadMatch(loc, "expected '%s', got '%s'" % (term.spec, json.dumps(element)))
    return GoodMatch()

def match_wildcard(loc, term, element):
    """Determine if the JSPEC wildcard matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECWildcard): The JSPEC wildcard.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC wildcard matches the JSON
            element
    """
    if not isinstance(element, PYTHON_NATIVE) and element is not None:
        return BadMatch(loc, "expected a Python native JSON element, not %s" % element.__class__)
    return GoodMatch()

def match_negation(loc, term, element):
    """Determine if the JSPEC negation matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECNegation): The JSPEC negation.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC negation matches the JSON element
    """
    result = match_element(loc, term.spec, element)
    if bool(result):
        return BadMatch(loc, "expected '%s', got '%s'" % (term, json.dumps(element)))
    return GoodMatch()

def match_macro(loc, term, element):
    """Determine if the JSPEC macro matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECMacro): The JSPEC macro.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC macro matches the JSON element
    """
    string_value = os.getenv(term.spec, None)
    if string_value == None:
        return BadMatch(loc, "failed to find the JSPEC macro '%s'" % term)
    try:
        value = json.loads(string_value)
    except json.decoder.JSONDecodeError:
        return BadMatch(loc, "failed to parse the JSPEC macro '%s' as a JSON element" % term)
    if value != element:
        return BadMatch(loc, "JSPEC macro '%s' failed to match '%s'" % (term, json.dumps(element)))
    return GoodMatch()

def match_conditional(loc, conditional, element):
    """Determine if the JSPEC conditional matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECConditional): The JSPEC conditional.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC conditional matches the JSON
            element
    """
    spec = conditional.spec
    term = conditional.spec[0]
    result = match_element(loc, term, element)
    value = bool(result)
    i = 1
    while i < len(spec):
        operator = spec[i]
        term = spec[i+1]
        i += 2
        result = match_element(loc, term, element)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return GoodMatch()
    return BadMatch(loc, "conditional elements %s do not match the element '%s'" % (conditional, element))

def match_object_placeholder(loc, term, element):
    """Determine if the JSPEC object placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECObjectPlaceholder): The JSPEC object placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC object placeholder matches the
            JSON element
    """
    if isinstance(element, dict):
        return GoodMatch()
    return BadMatch(loc, "expected an object")

def match_array_placeholder(loc, term, element):
    """Determine if the JSPEC array placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECArrayPlaceholder): The JSPEC array placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC array placeholder matches the
            JSON element
    """
    if isinstance(element, list):
        return GoodMatch()
    return BadMatch(loc, "expected an array")

def match_string_placeholder(loc, term, element):
    """Determine if the JSPEC string placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECStringPlaceholder): The JSPEC string placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC string placeholder matches the
            JSON element
    """
    if isinstance(element, str):
        return GoodMatch()
    return BadMatch(loc, "expected a string")

def match_boolean_placeholder(loc, term, element):
    """Determine if the JSPEC boolean placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECBooleanPlaceholder): The JSPEC boolean placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC boolean placeholder matches the
            JSON element
    """
    if isinstance(element, bool):
        return GoodMatch()
    return BadMatch(loc, "expected a boolean")

def match_int_placeholder(loc, term, element):
    """Determine if the JSPEC int placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECIntPlaceholder): The JSPEC int placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC int placeholder matches the
            JSON element
    """
    if not isinstance(element, int):
        return BadMatch(loc, "expected an int")
    if term.spec is None:
        return GoodMatch()
    symbol, value, = term.spec
    if isinstance(symbol, JSPECInequalityLessThan):
        if element < value:
            return GoodMatch()
        return BadMatch(loc, "expected an int that is less than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo):
        if element <= value:
            return GoodMatch()
        return BadMatch(loc, "expected an int that is less than or equal to '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThan):
        if element > value:
            return GoodMatch()
        return BadMatch(loc, "expected an int that is more than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo):
        if element >= value:
            return GoodMatch()
        return BadMatch(loc, "expected an int that is more than or equal to '%s', got '%s'" % (value, json.dumps(element)))

    raise ValueError("JSPEC does not support inequalities of class %s" % symbol.__class__)

def match_real_placeholder(loc, term, element):
    """Determine if the JSPEC real placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECRealPlaceholder): The JSPEC real placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC real placeholder matches the
            JSON element
    """
    if not isinstance(element, float):
        return BadMatch(loc, "expected a real")
    if term.spec is None:
        return GoodMatch()
    symbol, value, = term.spec
    if isinstance(symbol, JSPECInequalityLessThan):
        if element < value:
            return GoodMatch()
        return BadMatch(loc, "expected a real that is less than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo):
        if element <= value:
            return GoodMatch()
        return BadMatch(loc, "expected a real that is less than or equal to '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThan):
        if element > value:
            return GoodMatch()
        return BadMatch(loc, "expected a real that is more than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo):
        if element >= value:
            return GoodMatch()
        return BadMatch(loc, "expected a real that is more than or equal to '%s', got '%s'" % (value, json.dumps(element)))

    raise ValueError("JSPEC does not support inequalities of class %s" % symbol.__class__)

def match_number_placeholder(loc, term, element):
    """Determine if the JSPEC number placeholder matches the JSON element.

    Args:
        loc (str): The current location in the JSON
        term (JSPECNumberPlaceholder): The JSPEC number placeholder.
        element (obj): The Python native object representing a JSON element

    Returns:
        Result: The result of whether the JSPEC number placeholder matches the
            JSON element
    """
    if not isinstance(element, (int, float)):
        return BadMatch(loc, "expected a number")
    if term.spec is None:
        return GoodMatch()
    symbol, value, = term.spec
    if isinstance(symbol, JSPECInequalityLessThan):
        if element < value:
            return GoodMatch()
        return BadMatch(loc, "expected a number that is less than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo):
        if element <= value:
            return GoodMatch()
        return BadMatch(loc, "expected a number that is less than or equal to '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThan):
        if element > value:
            return GoodMatch()
        return BadMatch(loc, "expected a number that is more than '%s', got '%s'" % (value, json.dumps(element)))
    elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo):
        if element >= value:
            return GoodMatch()
        return BadMatch(loc, "expected a number that is more than or equal to '%s', got '%s'" % (value, json.dumps(element)))

    raise ValueError("JSPEC does not support inequalities of class %s" % symbol.__class__)