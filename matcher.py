from os import remove
import re

from scanner import scan

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

def match_object(spec, obj):
    capture_dict = {}
    spec_without_captures = {}
    for k, v in spec.items():
        if k.__class__ == JSPECObjectCaptureKey and v.__class__ == JSPECObjectCaptureValue:
            capture_dict[k] = v
        else:
            spec_without_captures[k] = v
    return match_object_traverse(spec_without_captures, obj, capture_dict)

def match_object_traverse(spec, obj, capture_dict):

    spec_terminated = len(spec) == 0
    obj_terminated = len(obj) == 0

    if obj_terminated:
        return spec_terminated

    for obj_key, obj_val in obj.items():
        for capture_key, capture_val in capture_dict.items():
            if match_capture(capture_key, obj_key) and match_capture(capture_val, obj_val) and match_object_traverse(spec, remove_key(obj, obj_key), capture_dict):
                return True
        for spec_key, spec_val in spec.items():
            if match_element(spec_key, obj_key) and match_element(spec_val, obj_val):
                return match_object_traverse(remove_key(spec, spec_key), remove_key(obj, obj_key), capture_dict) 

    return False
    
            
def remove_key(d, r):
    return dict((k, v) for k, v in d.items() if k != r)

def match_array(spec, obj):
    return match_array_traverse(spec, 0, obj, 0, [])

def match_array_traverse(spec_list, spec_idx, obj_list, obj_idx, capture_list):
    
    spec_terminated = spec_idx >= len(spec_list)
    obj_terminated = obj_idx >= len(obj_list)

    if not spec_terminated:
        spec = spec_list[spec_idx]
        if isinstance(spec, JSPECArrayCaptureElement):
            capture_list.append(spec)
            return match_array_traverse(spec_list, spec_idx+1, obj_list, obj_idx, capture_list[:])

    if obj_terminated:
        return spec_terminated
    
    obj = obj_list[obj_idx]

    while capture_list:
        if match_capture(capture_list[0], obj) and match_array_traverse(spec_list, spec_idx, obj_list, obj_idx+1, capture_list[:]):
            return True
        capture_list.pop(0)

    if spec_terminated:
        return False
    if not match_element(spec, obj):
        return False
    return match_array_traverse(spec_list, spec_idx+1, obj_list, obj_idx+1, capture_list[:])

def match_string(spec, obj):
    if not isinstance(obj, str):
        return False
    return re.compile(r'%s' % spec).fullmatch(obj) is not None

def match_int(spec, obj):
    if not isinstance(obj, int):
        return False
    return spec == obj

def match_real(spec, obj):
    if not isinstance(obj, float):
        return False
    return spec == obj

def match_boolean(spec, obj):
    if not isinstance(obj, bool):
        return False
    return spec == obj

def match_wildcard(spec, obj):
    # TODO should be an value json elements
    return True

def match_null(spec, obj):
    return obj is None

def match_capture(capture, obj):
    return match_element(capture.element, obj)

def match(jspec, obj):
    if not isinstance(jspec, JSPEC):
        raise TypeError()
    element = jspec.element
    return match_element(element, obj)

def match_element(element, obj):
    cls = element.__class__
    spec = element.spec
    if cls == JSPECObject:
        return match_object(spec, obj)
    if cls == JSPECArray:
        return match_array(spec, obj)
    if cls == JSPECString:
        return match_string(spec, obj)
    if cls == JSPECInt:
        return match_int(spec, obj)
    if cls == JSPECReal:
        return match_real(spec, obj)
    if cls == JSPECBoolean:
        return match_boolean(spec, obj)
    if cls == JSPECWildcard:
        return match_wildcard(spec, obj)
    if cls == JSPECNull:
        return match_null(spec, obj)

    return False