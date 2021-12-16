# TODO fix array and object matching + captures
# TODO add tests for these too
# TODO add documentation

import re
import json

from .component import (
    JSPECCaptureMultiplier,
    JSPECElement,
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
    JSPECConditional,
    JSPECEvaluation,
    JSPECObjectPlaceholder,
    JSPECArrayPlaceholder,
    JSPECStringPlaceholder,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECBooleanPlaceholder,
    JSPECNumberPlaceholder,
    JSPECArrayCaptureGroup,
    JSPECObjectCaptureGroup,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECInequalityLessThan,
    JSPECInequalityLessThanOrEqualTo,
    JSPECInequalityMoreThan,
    JSPECInequalityMoreThanOrEqualTo,
)

class Result:

    def __init__(self, res, loc=None, msg=None):
        self.res = bool(res) 
        self.loc = loc or ""
        self.msg = msg or ""

    def __bool__(self):
        return self.res

    def errormsg(self):
        if self.res:
            return ""
        return "At location %s - %s" % (self.loc, self.msg)

def GoodMatch():
    return Result(True)

def BadMatch(loc, msg):
    return Result(False, loc, msg)

def match_conditional(loc, spec, obj):
    result = match_element(loc, spec.specification[0], obj)
    value = bool(result)
    i = 1
    while i < len(spec.specification):
        operator = spec.specification[i]
        spec = spec.specification[i+1]
        i += 2
        result = match_element(loc, spec, obj)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return GoodMatch()
    return BadMatch(loc, "conditional elements %s do not match the element '%s'" % (spec, obj))

def match_evaluation(loc, spec, obj):

    pass

def match_placeholder(loc, spec, obj):
    if isinstance(spec, JSPECObjectPlaceholder):
        if isinstance(obj, dict):
            return GoodMatch()
        return BadMatch(loc, "")
    if isinstance(spec, JSPECArrayPlaceholder):
        if isinstance(obj, list):
            return GoodMatch()
        return BadMatch(loc, "")
    if isinstance(spec, JSPECStringPlaceholder):
        if isinstance(obj, str):
            return GoodMatch()
        return BadMatch(loc, "")
    if isinstance(spec, JSPECBooleanPlaceholder):
        if isinstance(obj, bool):
            return GoodMatch()
        return BadMatch(loc, "")
    if isinstance(spec, JSPECIntPlaceholder):
        if isinstance(obj, int):
            symbol, value, = spec.entities
            if isinstance(symbol, JSPECInequalityLessThan) and obj < value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo) and obj <= value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThan) and obj > value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo) and obj >= value:
                return GoodMatch()
            return BadMatch(loc, "")
        return BadMatch(loc, "")
    if isinstance(spec, JSPECRealPlaceholder):
        if isinstance(obj, float):
            symbol, value, = spec.entities
            if isinstance(symbol, JSPECInequalityLessThan) and obj < value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo) and obj <= value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThan) and obj > value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo) and obj >= value:
                return GoodMatch()
            return BadMatch(loc, "")
        return BadMatch(loc, "")
    if isinstance(spec, JSPECNumberPlaceholder):
        if isinstance(obj, (int, float)):
            symbol, value, = spec.entities
            if isinstance(symbol, JSPECInequalityLessThan) and obj < value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityLessThanOrEqualTo) and obj <= value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThan) and obj > value:
                return GoodMatch()
            elif isinstance(symbol, JSPECInequalityMoreThanOrEqualTo) and obj >= value:
                return GoodMatch()
            return BadMatch(loc, "")
        return BadMatch(loc, "")
    return BadMatch(loc, "")

PYTHON_NATIVE = (
    dict, 
    list, 
    str, 
    int, 
    float, 
    bool,
)

PLACEHOLDERS = (
    JSPECObjectPlaceholder,
    JSPECArrayPlaceholder,
    JSPECStringPlaceholder,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECBooleanPlaceholder,
    JSPECNumberPlaceholder,
)

def match_negation(loc, spec, obj):
    element = spec.element
    result = match_element(loc, element, obj)
    if bool(result):
        return BadMatch(loc, "n")
    return GoodMatch()

def match_object(loc, term, obj):

    bad_results = list()

    exhausted_spec = (
        all(isinstance(pair, JSPECObjectCaptureGroup) for pair in term)
        and all((pair.multiplier.minimum == None or pair.multiplier.minimum == 0) for pair in term)
    )
    exhausted_obj = len(obj) == 0

    if exhausted_spec:
        if exhausted_obj:
            return GoodMatch()
        return BadMatch(loc, "exhausted JSPEC object, the following JSON keys are unmatched: %s" % ", ".join(['"%s"' % k for k in obj.keys()]))
    elif exhausted_obj:
        return BadMatch(loc, "exhausted JSON object, the following JSPEC keys are unmatched: %s" % ", ".join([str(pair.key()) for pair in term]))

    for obj_pair in obj.items():
        reduced_obj = dict(
            pair for pair in obj.items() 
            if pair != obj_pair
        )
        for spec_pair in term:
            if isinstance(spec_pair, JSPECObjectPair):
                reduced_spec = JSPECObject([
                    JSPECObjectPair((pair.key(), pair.value())) for pair in term 
                    if pair != spec_pair
                ])
                result = match_object_pair(loc, spec_pair, obj_pair)
            elif spec_pair.__class__ == JSPECObjectCaptureGroup:
                reduced_group = JSPECObjectCaptureGroup(
                    spec_pair.entities,
                    JSPECCaptureMultiplier(
                        spec_pair.multiplier.minimum - 1 if spec_pair.multiplier.minimum is not None else None,
                        spec_pair.multiplier.maximum - 1 if spec_pair.multiplier.maximum is not None else None,
                    )
                )
                reduced_spec = JSPECObject([
                    (pair if pair != spec_pair else reduced_group) 
                    for pair in term
                ])
                result = match_object_capture_group(loc, spec_pair, obj_pair)
            if not bool(result):
                bad_results.append(result)
                continue
            return match_object(loc, reduced_spec.term, reduced_obj)

    # TODO add logic to get best bad result
    return BadMatch(loc, "the following JSON object keys were unmatched: %s" % ", ".join(['"%s"' % k for k in obj.keys()]))

def match_object_pair(loc, spec_pair, obj_pair):
    key_result = match_element(loc, spec_pair.key(), obj_pair[0])
    if not bool(key_result):
        return key_result
    value_result = match_element(loc + "." + obj_pair[0], spec_pair.value(), obj_pair[1])
    if not bool(value_result):
        return value_result
    return GoodMatch()

def match_object_capture_group(loc, spec_capture_group, obj_pair):
    result = match_object_pair(loc, spec_capture_group.entities[0], obj_pair)
    value = bool(result)
    i = 1
    while i < len(spec_capture_group.entities):
        operator = spec_capture_group.entities[i]
        spec_pair = spec_capture_group.entities[i+1]
        i += 2
        result = match_object_pair(loc, spec_pair, obj_pair)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return GoodMatch()
    return BadMatch(loc, "failed capture")
        


def match_array(loc, term, obj):
    if not isinstance(obj, list):
        return BadMatch(loc, "expected an array, got '%s'" % json.dumps(obj))
    return match_array_traverse(loc, term, obj, 0)

def match_array_traverse(loc, term, obj, idx):

    exhausted_spec = (
        all(isinstance(element, JSPECArrayCaptureGroup) for element in term)
        and all((pair.multiplier.minimum == None or pair.multiplier.minimum == 0) for pair in term)
    )
    exhausted_obj = len(obj) == 0

    if exhausted_spec:
        if exhausted_obj:
            return GoodMatch()
        return BadMatch(loc, "exhausted JSPEC array, no JSPEC element left to match '%s'" % obj[0])
    elif exhausted_obj:
        return BadMatch(loc, "exhausted JSON array, no JSON element left to match '%s'" % term[0])

    reduced_obj = obj[1:]
    if isinstance(term[0], JSPECElement):
        reduced_spec = term[1:]
        result = match_element("%s[%s]" % (loc, idx), term[0], obj[0])
        if not bool(result):
            return result
        return match_array_traverse(loc, reduced_spec, reduced_obj, idx+1)
    elif isinstance(term[0], JSPECArrayCaptureGroup):
        reduced_group = JSPECArrayCaptureGroup(
            term[0].entities,
            JSPECCaptureMultiplier(
                term[0].multiplier.minimum - 1 if term[0].multiplier.minimum is not None else None,
                term[0].multiplier.maximum - 1 if term[0].multiplier.maximum is not None else None,
            )
        )
        result = match_array_capture_group(loc, term[0], obj[0])
        if not bool(result):
            return result
        return match_array_traverse(loc, reduced_group, reduced_obj, idx+1)

    raise ValueError("JSPEC arrays do not support elements of class %s" % term[0].__class__)
    
def match_array_capture_group(loc, spec_capture_group, element):
    result = match_element(loc, spec_capture_group.entities[0], element)
    value = bool(result)
    i = 1
    while i < len(spec_capture_group.entities):
        operator = spec_capture_group.entities[i]
        spec_element = spec_capture_group.entities[i+1]
        i += 2
        result = match_element(loc, spec_element, element)
        if operator.__class__ == JSPECLogicalOperatorAnd:
            value = value and bool(result)
        elif operator.__class__ == JSPECLogicalOperatorOr:
            value = value or bool(result)
        elif operator.__class__ == JSPECLogicalOperatorXor:
            value = (value or bool(result)) and not (value and bool(result))
    if value:
        return GoodMatch()
    return BadMatch(loc, "failed capture")


def match_element(loc, spec, obj):
    """.

    Args:
        spec (JSPECElement): The JSPEC element.
        obj (obj): The python native object.

    """
    term = spec.term

    if isinstance(spec, JSPECObject):
        if not isinstance(obj, dict):
            return BadMatch(loc, "expected an object")
        return match_object(loc, term, obj)
   
    if isinstance(spec, JSPECArray):
        return match_array(loc, term, obj)
    
    if isinstance(spec, JSPECString):
        return match_string(loc, term, obj)

    if isinstance(spec, JSPECInt):
        return match_int(loc, term, obj)

    if isinstance(spec, JSPECReal):
        return match_real(loc, term, obj)

    if isinstance(spec, JSPECBoolean):
        return match_boolean(loc, term, obj)

    if isinstance(spec, JSPECNull):
        return match_null(loc, term, obj)  

    if isinstance(spec, JSPECWildcard):
        return match_wildcard(loc, term, obj)

    if isinstance(spec, JSPECNegation):
        return match_negation(loc, spec, obj)

    if isinstance(spec, JSPECConditional):
        return match_conditional(loc, spec, obj)

    if isinstance(spec, JSPECEvaluation):
        return match_evaluation(loc, spec, obj)

    if isinstance(spec, PLACEHOLDERS):
        return match_placeholder(loc, spec, obj)

    raise ValueError("JSPEC does not support elements of class %s" % spec.__class__)

def match_null(loc, term, obj):
    if obj is not None:
        return BadMatch(loc, "expected '%s', got '%s'" % (term, json.dumps(obj)))
    return GoodMatch()

def match_boolean(loc, term, obj):
    if not isinstance(obj, bool):
        return BadMatch(loc, "expected a boolean, got '%s'" % json.dumps(obj))
    if term != obj:
        return BadMatch(loc, "expected '%s', got '%s'" % (term, json.dumps(obj)))
    return GoodMatch()

def match_int(loc, term, obj):
    if not isinstance(obj, int):
        return BadMatch(loc, "expected a int, got '%s'" % json.dumps(obj))
    if term != obj:
        return BadMatch(loc, "expected '%s', got '%s'" % (term, json.dumps(obj)))
    return GoodMatch()

def match_real(loc, term, obj):
    if not isinstance(obj, float):
        return BadMatch(loc, "expected a real, got '%s'" % json.dumps(obj))
    if term != obj:
        return BadMatch(loc, "expected '%s', got '%s'" % (term, json.dumps(obj)))
    return GoodMatch()

def match_string(loc, term, obj):
    if not isinstance(obj, str):
        return BadMatch(loc, "expected a string, got '%s'" % json.dumps(obj))
    if re.compile(r'%s' % term).fullmatch(obj) is None:
        return BadMatch(loc, "regex pattern '%s' failed to match '%s'" % (term, json.dumps(obj)))
    return GoodMatch()

def match_wildcard(loc, term, obj):
    if not isinstance(obj, PYTHON_NATIVE) and obj is not None:
        return BadMatch(loc, "expected a Python native JSON element, not %s" % obj.__class__)
    return GoodMatch()

def match(jspec, obj):
    element = jspec.element
    result = match_element('$', element, obj)
    return bool(result), result.errormsg()