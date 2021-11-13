"""JSPEC Testing Module for matching JSPEC documents for a placeholder.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherPlaceholder(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    placeholders.

    A valid JSPEC placeholder one of array, boolean, int, null, object, real or
    string.
    """

    def test_matcher_placeholder_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        placeholder as its element.
        """
        test_cases = [
            {
                "name": "Object placeholder",
                "doc": "object",
                "obj": {},
            },
            {
                "name": "Array placeholder",
                "doc": "array",
                "obj": [],
            },
            {
                "name": "String placeholder",
                "doc": "string",
                "obj": "",
            },
            {
                "name": "Integer placeholder",
                "doc": "int",
                "obj": 0,
            },
            {
                "name": "Real placeholder",
                "doc": "real",
                "obj": 0.0,
            },
            {
                "name": "Bool placeholder",
                "doc": "bool",
                "obj": False,
            },
            {
                "name": "Object placeholder, not empty",
                "doc": "object",
                "obj": {"key": "val", "a": 5, "s": {"b":[]}},
            },
            {
                "name": "Array placeholder, not empty",
                "doc": "array",
                "obj": [1, 2, 3, 4, 5],
            },
            {
                "name": "String placeholder, not empty",
                "doc": "string",
                "obj": "something",
            },
            {
                "name": "Integer placeholder, not zero",
                "doc": "int",
                "obj": 1348239,
            },
            {
                "name": "Real placeholder, not zero",
                "doc": "real",
                "obj": -27.34310,
            },
            {
                "name": "Bool placeholder, not False",
                "doc": "bool",
                "obj": True,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_placeholder_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified placeholder as its element.
        """
        test_cases = [
            {
                "name": "Unwanted array",
                "doc": "object",
                "obj": [],
                "want": "At location $ - expected an object",
            },
            {
                "name": "Unwanted object",
                "doc": "array",
                "obj": {},
                "want": "At location $ - expected an array",
            },
            {
                "name": "Unwanted string",
                "doc": "string",
                "obj": [],
                "want": "At location $ - expected a string",
            },
            {
                "name": "Unwanted real",
                "doc": "int",
                "obj": 0.0,
                "want": "At location $ - expected an int",
            },
            {
                "name": "Unexpected int",
                "doc": "real",
                "obj": 0,
                "want": "At location $ - expected a real",
            },
            {
                "name": "Unexpected null",
                "doc": "bool",
                "obj": None,
                "want": "At location $ - expected a boolean",
            },
        ]
        self._bad_match(test_cases)