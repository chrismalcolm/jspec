import re

from component import (
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
        return "At location '%s' - %s" % (self.msg, self.loc)

def GoodMatch():
    return Result(True)

def BadMatch(loc, msg):
    return Result(False, loc, msg)

def match_object(loc, spec, obj):
    capture_dict = {}
    spec_without_captures = {}
    for k, v in spec.items():
        if isinstance(k, JSPECObjectCaptureKey) and isinstance(v, JSPECObjectCaptureValue):
            capture_dict[k] = v
        else:
            spec_without_captures[k] = v
    return match_object_traverse(loc, spec_without_captures, obj, capture_dict)

def match_object_traverse(loc, spec, obj, capture_dict):

    spec_terminated = len(spec) == 0
    obj_terminated = len(obj) == 0

    if obj_terminated:
        return GoodMatch() if spec_terminated else BadMatch(loc, "the following jspec keys were unmatched: %s" % ", ".join([str(k) for k in spec.keys()]))

    for obj_key, obj_val in obj.items():
        for capture_key, capture_val in capture_dict.items():
            if (
                    bool(match_capture(loc, capture_key, obj_key)) and
                    bool(match_capture(loc + '.%s' % obj_key, capture_val, obj_val)) and
                    bool(match_object_traverse(loc, spec, remove_key(obj, obj_key), capture_dict))
                ):
                    return GoodMatch()
        for spec_key, spec_val in spec.items():
            if (
                    bool(match_element(loc, spec_key, obj_key)) and
                    bool(match_element(loc + '.%s' % obj_key, spec_val, obj_val))
                ):
                    return match_object_traverse(loc, remove_key(spec, spec_key), remove_key(obj, obj_key), capture_dict) 

    return BadMatch(loc, "the following object keys were unmatched: %s" % ", ".join([str(k) for k in obj.keys()]))

def remove_key(d, r):
    return dict((k, v) for k, v in d.items() if k != r)

def match_array(loc, spec, obj):
    return match_array_traverse(loc, spec, 0, obj, 0, [])

def match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx, capture_list):
    
    spec_terminated = spec_idx >= len(spec_list)
    obj_terminated = obj_idx >= len(obj_list)

    if not spec_terminated:
        spec = spec_list[spec_idx]
        if isinstance(spec, JSPECArrayCaptureElement):
            capture_list.append(spec)
            return match_array_traverse(loc, spec_list, spec_idx+1, obj_list, obj_idx, capture_list[:])

    if obj_terminated:
        return GoodMatch() if spec_terminated else BadMatch(loc, "exhausted array elements for matching jspec elements at index %i" % spec_idx)
    
    obj = obj_list[obj_idx]

    while capture_list:
        if (
                bool(match_capture(loc + '[%s]' % obj_idx, capture_list[0], obj)) and 
                bool(match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx+1, capture_list[:]))
            ):
            return GoodMatch()
        capture_list.pop(0)

    if spec_terminated:
        return BadMatch(loc, "exhausted jspec elements for matching array at index %i" % obj_idx)
    result = match_element(loc + '[%s]' % obj_idx, spec, obj)
    if not bool(result):
        return result
    return match_array_traverse(loc, spec_list, spec_idx+1, obj_list, obj_idx+1, capture_list[:])

def match_capture(loc, capture, obj):
    return match_element(loc, capture.element, obj)

def match_string(loc, spec, obj):
    return GoodMatch() if re.compile(r'%s' % spec).fullmatch(obj) is not None else BadMatch(loc, "regex pattern '%s' failed to match '%s'" % (spec, obj))

def match_int(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_real(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_boolean(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_element(loc, element, obj):
    spec = element.spec
    is_placeholder = element.is_placeholder

    if isinstance(element, JSPECObject):
        if not isinstance(obj, dict):
            return False
        return GoodMatch() if is_placeholder else match_object(loc, spec, obj)
   
    if isinstance(element, JSPECArray):
        if not isinstance(obj, list):
            return False
        return GoodMatch() if is_placeholder else match_array(loc, spec, obj)
    
    if isinstance(element, JSPECString):
        if not isinstance(obj, str):
            return False
        return GoodMatch() if is_placeholder else match_string(loc, spec, obj)

    if isinstance(element, JSPECInt):
        if not isinstance(obj, int):
            return False
        return GoodMatch() if is_placeholder else match_int(loc, spec, obj)

    if isinstance(element, JSPECReal):
        if not isinstance(obj, float):
            return False
        return GoodMatch() if is_placeholder else match_real(loc, spec, obj)

    if isinstance(element, JSPECBoolean):
        if not isinstance(obj, bool):
            return False
        return GoodMatch() if is_placeholder else match_boolean(loc, spec, obj)

    if isinstance(element, JSPECNull):
        return GoodMatch() if obj is None else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

    if isinstance(element, JSPECWildcard):
        return GoodMatch()

    raise ValueError("JSPEC does not support elements of class %s" % element.__class__)

def match(jspec, obj):
    element = jspec.element
    result = match_element('$', element, obj)
    return bool(result), result.errormsg()