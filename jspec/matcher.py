# TODO fix array and object matching + captures
# TODO add tests for these too
# TODO add documentation

import re

from .component import (
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
    JSPECNull,
    JSPECWildcard,
    JSPECConditional,
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
        return "At location %s - %s" % (self.loc, self.msg)

def GoodMatch():
    return Result(True)

def BadMatch(loc, msg):
    return Result(False, loc, msg)

def captures_are_filled(captures):
    return not any([capture.multiplier > 0 for capture in captures])

def remove_key(d, r):
    return dict((k, v) for k, v in d.items() if k != r)

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
    captures_terminated = captures_are_filled(capture_dict.keys())

    if obj_terminated:
        if not spec_terminated:
            return BadMatch(loc, "the following jspec keys were unmatched: %s" % ", ".join([str(k) for k in spec.keys()]))
        if not captures_terminated:
            return BadMatch(loc, "the following captures have not been fully matched: %s" % capture_dict)
        return GoodMatch()

    #for obj_key, obj_val in obj.items():
    #    for capture_key, capture_val in capture_dict.items():
    #        if (
    #                bool(match_object_capture(loc, capture_key, capture_val, obj_key, obj_val)) and 
    #                bool(match_object_traverse(loc, spec, remove_key(obj, obj_key), capture_dict))
    #            ):
    #                return GoodMatch()
    #    for spec_key, spec_val in spec.items():
    #        if (
    #                bool(match_element(loc, spec_key, obj_key)) and
    #                bool(match_element(loc + '.%s' % obj_key, spec_val, obj_val))
    #            ):
    #                return match_object_traverse(loc, remove_key(spec, spec_key), remove_key(obj, obj_key), capture_dict)

    #for obj_key, obj_val in obj.items():
    #    for capture_key, capture_val in capture_dict.items():
    #        capture_key_elements = set([capture_key.element]) if capture_key.element is not None else capture_key.elements
    #        for capture_key_element in capture_key_elements:
    #            capture_key.element = capture_key_element
    #            capture_val_elements = set([capture_val.element]) if capture_val.element is not None else capture_val.elements
    #            for capture_val_element in capture_val_elements:
    #                capture_val.element = capture_val_element
    #                if (
    #                        bool(match_object_capture(loc, capture_key, capture_val, obj_key, obj_val)) and 
    #                        bool(match_object_traverse(loc, spec, remove_key(obj, obj_key), capture_dict))
    #                ):
    #                    return GoodMatch()

    for obj_key, obj_val in obj.items():
        for key, val in capture_dict.items():
            for split_capture_key in key.split():
                for split_capture_val in val.split():
                    split_capture_dict = remove_key(capture_dict, key)
                    split_capture_dict[split_capture_key] = split_capture_val
                    if (
                            bool(match_object_capture(loc, split_capture_key, split_capture_val, obj_key, obj_val)) and 
                            bool(match_object_traverse(loc, spec, remove_key(obj, obj_key), split_capture_dict))
                    ):
                        return GoodMatch()

        for spec_key, spec_val in spec.items():
            if (
                    bool(match_element(loc, spec_key, obj_key)) and
                    bool(match_element(loc + '.%s' % obj_key, spec_val, obj_val))
                ):
                    return match_object_traverse(loc, remove_key(spec, spec_key), remove_key(obj, obj_key), capture_dict) 

    return BadMatch(loc, "the following object keys were unmatched: %s" % ", ".join(['"%s"' % k for k in obj.keys()]))

#def match_object_capture(loc, capture_key, capture_val, obj_key, obj_val):
#    if capture_key.multiplier == 0:
#        return BadMatch(loc, "exhausted capture")
#    if len(capture_key.elements) == 0:
#        return BadMatch(loc, "no elements in capture")
#    for element in capture_key.elements:
#        result = match_element(loc, element, obj_key)
#        if bool(result):
#            break
#    else:
#        return result
#    for element in capture_val.elements:
#        result = match_element(loc + '.%s' % obj_key, element, obj_val)
#        if bool(result):
#            break
#    else:
#        return result
#    capture_key.multiplier -= 1
#    capture_val.multiplier -= 1
#    return result

def match_object_capture(loc, capture_key, capture_val, obj_key, obj_val):
    if capture_key.multiplier == 0:
        return BadMatch(loc, "exhausted capture")
    result = match_element(loc, capture_key.element, obj_key)
    if not bool(result):
        return result
    result = match_element(loc + '.%s' % obj_key, capture_val.element, obj_val)
    if not bool(result):
        return result
    capture_key.multiplier -= 1
    capture_val.multiplier -= 1
    return result

def match_array(loc, spec, obj):
    return match_array_traverse(loc, spec, 0, obj, 0, [])

def match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx, capture_list):
    
    spec_terminated = spec_idx >= len(spec_list)
    obj_terminated = obj_idx >= len(obj_list)
    captures_terminated = captures_are_filled(capture_list)

    if not spec_terminated:
        spec = spec_list[spec_idx]
        if isinstance(spec, JSPECArrayCaptureElement):
            capture_list.append(spec)
            return match_array_traverse(loc, spec_list, spec_idx+1, obj_list, obj_idx, capture_list[:])

    if obj_terminated:
        if not spec_terminated:
            return BadMatch(loc, "exhausted array elements for matching jspec elements at index %i" % spec_idx)
        if not captures_terminated:
            BadMatch(loc, "the following captures have not been fully matched: %s" % capture_list)
        return GoodMatch()
    
    obj = obj_list[obj_idx]

    #while capture_list:
    #    if (
    #            bool(match_array_capture(loc + '[%i]' % obj_idx, capture_list[0], obj)) and 
    #            bool(match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx+1, capture_list[:]))
    #        ):
    #        return GoodMatch()
    #    capture_list.pop(0)

    #while capture_list:
    #    elements = set([capture_list[0].element]) if capture_list[0].element is not None else capture_list[0].elements
    #    for element in elements:
    #        capture_list[0].element = element
    #        if (
    #                bool(match_array_capture(loc + '[%i]' % obj_idx, capture_list[0], obj)) and 
    #                bool(match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx+1, capture_list[:]))
    #            ):
    #            return GoodMatch()
    #    capture_list.pop(0)

    while capture_list:
        for capture in capture[0].split():
            capture_list[0] = capture
            if (
                    bool(match_array_capture(loc + '[%i]' % obj_idx, capture, obj)) and 
                    bool(match_array_traverse(loc, spec_list, spec_idx, obj_list, obj_idx+1, capture_list[:]))
                ):
                return GoodMatch()
        capture_list.pop(0)

    if spec_terminated:
        return BadMatch(loc, "exhausted jspec elements for matching array at index %i" % obj_idx)
    result = match_element(loc + '[%i]' % obj_idx, spec, obj)
    if not bool(result):
        return result
    return match_array_traverse(loc, spec_list, spec_idx+1, obj_list, obj_idx+1, capture_list[:])

def match_array_capture(loc, capture, obj):
    if capture.multiplier == 0:
        return BadMatch(loc, "exhausted capture")
    result = match_element(loc, capture.element, obj)
    if not bool(result):
        return result
    capture.multiplier -= 1
    return result

#def match_array_capture(loc, capture, obj):
#    if capture.multiplier == 0:
#        return BadMatch(loc, "exhausted capture")
#    if len(capture.elements) == 0:
#        return BadMatch(loc, "no elements in capture")
#    for element in capture.elements:
#        result = match_element(loc, element, obj)
#        if bool(result):
#            break
#    else:
#        return result
#    capture.multiplier -= 1
#    return result

def match_string(loc, spec, obj):
    return GoodMatch() if re.compile(r'%s' % spec).fullmatch(obj) is not None else BadMatch(loc, "regex pattern '%s' failed to match '%s'" % (spec, obj))

def match_int(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_real(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_boolean(loc, spec, obj):
    return GoodMatch() if spec == obj else BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))

def match_conditional(loc, spec, obj):
    for element in spec:
        result = match_element(loc, element, obj)
        if bool(result):
            return result
    sorted_elements = sorted([str(e) for e in spec])
    return BadMatch(loc, "conditional elements %s do not match the element '%s'" % (sorted_elements, obj))

def match_element(loc, element, obj):
    spec = element.spec
    is_placeholder = element.is_placeholder

    if isinstance(element, JSPECObject):
        if not isinstance(obj, dict):
            return BadMatch(loc, "expected an object")
        return GoodMatch() if is_placeholder else match_object(loc, spec, obj)
   
    if isinstance(element, JSPECArray):
        if not isinstance(obj, list):
            return BadMatch(loc, "expected an array")
        return GoodMatch() if is_placeholder else match_array(loc, spec, obj)
    
    if isinstance(element, JSPECString):
        if not isinstance(obj, str):
            return BadMatch(loc, "expected a string")
        return GoodMatch() if is_placeholder else match_string(loc, spec, obj)

    if isinstance(element, JSPECInt):
        if not isinstance(obj, int):
            return BadMatch(loc, "expected an int")
        return GoodMatch() if is_placeholder else match_int(loc, spec, obj)

    if isinstance(element, JSPECReal):
        if not isinstance(obj, float):
            return BadMatch(loc, "expected a real")
        return GoodMatch() if is_placeholder else match_real(loc, spec, obj)

    if isinstance(element, JSPECBoolean):
        if not isinstance(obj, bool):
            return BadMatch(loc, "expected a boolean")
        return GoodMatch() if is_placeholder else match_boolean(loc, spec, obj)

    if isinstance(element, JSPECNull):
        if obj is not None:
            return BadMatch(loc, "expected '%s', got '%s'" % (spec, obj))
        return GoodMatch()  

    if isinstance(element, JSPECWildcard):
        if not isinstance(obj, (dict, list, str, int, float, bool)) and obj is not None:
            return BadMatch(loc, "expected a Python native JSON element, not %s" % obj.__class__)
        return GoodMatch()

    if isinstance(element, JSPECConditional):
        return match_conditional(loc, spec, obj)

    raise ValueError("JSPEC does not support elements of class %s" % element.__class__)

def match(jspec, obj):
    element = jspec.element
    result = match_element('$', element, obj)
    return bool(result), result.errormsg()