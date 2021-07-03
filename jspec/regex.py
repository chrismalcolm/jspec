"""
    Module for checking candidate JSON against a specification JSON.
"""

import json
import io
from error import JSpecLoadError

from constants import (
    JSPEC_OBJECT_ITEMS_SUBSITUTION, 
    JSPEC_OBJECT_TEMPLATE_VALUE, 
    JSPEC_ARRAY_ELEMENT_SUBSITUTION, 
    JSPEC_ARRAY_TEMPLATE_VALUE
)
import re

class JSpec():
    """JSPEC interface"""

    def __init__(self, jspec_string):
        self._payload = self._loads(jspec_string)

    def _loads(self, jspec_string):
        try:
            return json.loads(jspec_string)
        except json.JSONDecodeError as jde:
            raise JSpecLoadError("later")

    def match(self, obj):
        if isinstance(obj, io.TextIOWrapper):
            obj = json.loads(obj.read())
        return self._match(self._payload, obj)

    def _match(self, spec, cand):
        """
            Check to see if the specification JSON matches the candidate JSON.

            Parameters:
            > spec (obj) : object representing a specification JSON
            > cand (obj) : object representing the candidate JSON

            Returns:
            (success, error_msg)
            - success (bool) : whether the candidate matches the specification
            - error_msg (str) : error message on the success of the match
                if not successsful a short description of where regex didn't match
                if successful, this is an empty string
        """
        return self._match_section(spec, cand, '$')

    def _match_section(self, spec, cand, name):
        """
            Check to see if the specification JSON section matches the candidate
            JSON section.

            Parameters:
            > spec (obj) : object representing a section of a specification JSON
            > cand (obj) : object representing a section of the candidate JSON
            > name (str) : position of the candidate section in the JSON

            Returns:
            (success, error_msg)
            - success (bool) : whether the candidate matches the specification
            - error_msg (str) : error message on the success of the match
                if not successsful a short description of where regex didn't match
                if successful, this is an empty string
        """
        if isinstance(spec, dict):
            return self._match_object(spec, cand, name)
        if isinstance(cand, dict):
            return (
                False,
                "Unexpected JSON object at position '%s'. Expected type: %s"
                % (name, self._py_type_to_json_type(spec))
            )

        if isinstance(spec, list):
            return self._match_array(spec, cand, name)
        if isinstance(cand, list):
            return (
                False,
                "Unexpected JSON array at position '%s'. Expected type: %s"
                % (name, self._py_type_to_json_type(spec))
            )

        return self._match_basic(spec, cand, name)

    def _match_object(self, spec, cand, name):
        """
            Check to see if the specification JSON object matches the candidate
            JSON section.

            Parameters:
            > spec (dict) : dict representing a specification JSON object
            > cand (obj) : object representing a section of the candidate JSON
            > name (str) : position of the candidate object in the JSON

            Returns:
            (success, error_msg)
            - success (bool) : whether the candidate matches the specification
            - error_msg (str) : error message on the success of the match
                if not successsful a short description of where regex didn't match
                if successful, this is an empty string
        """ 
        ignore_items = spec.get(JSPEC_OBJECT_ITEMS_SUBSITUTION, False)
        use_template = spec.get(JSPEC_OBJECT_TEMPLATE_VALUE, False)
        spec_keys = set(spec.keys()) - {JSPEC_OBJECT_ITEMS_SUBSITUTION, JSPEC_OBJECT_TEMPLATE_VALUE}
        if not isinstance(cand, dict):
            return (
                False,
                "Expected JSON object at position '%s'"
                % name
            )
        if use_template:
            if not cand.keys() or not spec_keys:
                return True, ""
            template_key = spec_keys.pop()
            for cand_key in cand.keys():
                if not self._regex_matches(template_key, cand_key):
                    return (
                        False,
                        "Cannot match template key regex at position '%s'. Want %s. Got %s"
                        % (name, template_key, cand_key)
                    )
                success, error_msg = self._match_section(spec[template_key], cand[cand_key], name+'.'+cand_key)
                if not success:
                    return success, error_msg
            return True, ""
        if spec_keys > cand.keys() and not use_template:
            return (
                False,
                "Missing keys at position '%s': %s" 
                % (name, ", ".join(spec_keys - cand.keys()))
            )
        if spec_keys < cand.keys() and not ignore_items and not use_template:
            return (
                False,
                "Unexpected keys at position '%s': %s"
                % (name, ", ".join(cand.keys() - spec_keys))
            )
        if len(spec_keys) != len(cand.keys()) and not ignore_items and not use_template:
            return (
                False, 
                "Mismatched keys at position '%s'. Expected %i keys, got %i"
                % (name, len(spec_keys), len(cand.keys()))
            )
        cand_key_set = set(cand.keys())
        for spec_key in spec_keys:
            cand_key = next((key for key in cand_key_set if self._regex_matches(spec_key, key)), None)
            if cand_key is None:
                return (
                    False, 
                    "Cannot match key regex at position '%s'. Want %s. Got %s"
                    % (name, ", ".join(spec_keys), ", ".join(cand.keys()))
                )
            success, error_msg = self._match_section(spec[spec_key], cand[cand_key], name+'.'+cand_key)
            if not success:
                return success, error_msg
            cand_key_set.remove(cand_key)
        return True, ""

    def _match_array(self, spec, cand, name):
        """
            Check to see if the specification JSON array matches the candidate
            JSON section.

            Parameters:
            > spec (list) : list representing a specification JSON array
            > cand (obj) : object representing a section of the candidate JSON
            > name (str) : position of the candidate array in the JSON

            Returns:
            (success, error_msg)
            - success (bool) : whether the candidate matches the specification
            - error_msg (str) : error message on the success of the match
                if not successsful a short description of where regex didn't match
                if successful, this is an empty string
        """
        ignore_elements = JSPEC_ARRAY_ELEMENT_SUBSITUTION in spec
        use_template = JSPEC_ARRAY_TEMPLATE_VALUE in spec
        if not isinstance(cand, list):
            return (
                False,
                "Expected JSON array at position '%s'"
                % name
            )
        if len(spec) != len(cand) and not ignore_elements and not use_template:
            return (
                False, 
                "Mismatched array elements at position '%s'. Expected %i, got %i"
                % (name, len(spec), len(cand))
            )
        if use_template:
            raw_spec = list(filter(lambda a: a != JSPEC_ARRAY_TEMPLATE_VALUE, spec))
            if raw_spec:
                template = raw_spec[0]
                for cand_index, cand_element in enumerate(cand):
                    success, error_msg = self._match_section(template, cand_element, name+'[%i]' % cand_index)
                    if not success:
                        return (
                            False,
                            "Template match failed: %s"
                            % (error_msg)
                        )
            return True, ""
        cand_index = 0
        ignoring = False
        for element in spec:
            if element == JSPEC_ARRAY_ELEMENT_SUBSITUTION:
                ignoring = True
                continue
            if cand_index >= len(cand):
                return (
                    False,
                    "Exhausted array elements at specification array element %s with the array at %s"
                    % (element, name)
                )
            success = False
            while not success and cand_index < len(cand):
                success, error_msg = self._match_section(element, cand[cand_index], name+'[%i]' % cand_index)
                if not success and not ignoring:
                    return success, error_msg
                cand_index += 1
            ignoring = False
        if cand_index < len(cand) and not ignoring:
            return (
                False,
                "Failed to match all specification array elements with the array elements at %s"
                % (name)
            )

        return True, ""

    def _match_basic(self, spec, cand, name):
        """
            Check to see if the specification JSON basic type matches the candidate
            JSON section. A basic type can be either str, int, float, bool or None.

            Parameters:
            > spec (obj) : object representing a specification JSON basic type
            > cand (obj) : object representing a section of the candidate JSON
            > name (str) : position of the candidate object in the JSON

            Returns:
            (success, error_msg)
            - success (bool) : whether the candidate matches the specification
            - error_msg (str) : error message on the success of the match
                if not successsful a short description of where regex didn't match
                if successful, this is an empty string
        """
        success = self._regex_matches(spec, cand)
        if success:
            return True, ""
        return (
            False, 
            "Cannot match regex at '%s'. %s does not match %s"
            % (name, self._json_basic_type_to_string(cand), self._json_basic_type_to_string(spec))
        )

    def _regex_matches(self, regex, value):
        """Returns whether the value parameter matches the regex parameter."""
        match_str = r'%s' % self._json_basic_type_to_string(regex)
        find_str = self._json_basic_type_to_string(value)
        return re.compile(match_str).fullmatch(find_str) is not None

    @staticmethod
    def _json_basic_type_to_string(obj):
        """Converts the JSON basic type to a str. A basic type can be either str,
        int, float, bool or None."""
        if isinstance(obj, bool):
            return str(obj).lower()
        if isinstance(obj, (str, int, float)):
            return str(obj) 
        return "null"

    @staticmethod
    def _py_type_to_json_type(obj):
        """Converts the python type to its name as a corresponing JSON section."""
        if isinstance(obj, dict):
            return "object"
        if isinstance(obj, list):
            return "array"
        if isinstance(obj, int):
            return "int"
        if isinstance(obj, float):
            return "float"
        if isinstance(obj, str):
            return "str"
        if isinstance(obj, bool):
            return "boolean"
        return "null"