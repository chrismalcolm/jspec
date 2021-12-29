"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherMacro``.
"""

import os

from test.matcher import JSPECTestMatcher

os.environ["TEST_OBJECT"] = '{"hello": "world"}'
os.environ["TEST_ARRAY"] = '["hello", "world", 123]'
os.environ["TEST_STRING"] = '"Hello World!"'
os.environ["TEST_INT"] = '456'
os.environ["TEST_REAL"] = '7.89'
os.environ["TEST_BOOLEAN"] = 'true'
os.environ["TEST_NULL"] = 'null'
os.environ["TEST_BAD"] = 'bad_element'

class JSPECTestMatcherMacro(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    macros.

    A JSPEC macro will match a macro.
    """

    def test_matcher_macro_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECMacro`` as its element.
        """
        test_cases = [
            {
                "name": "Evaluate object",
                "doc": "<TEST_OBJECT>",
                "obj": {"hello": "world"},
            },
            {
                "name": "Evaluate array",
                "doc": "<TEST_ARRAY>",
                "obj": ["hello", "world", 123],
            },
            {
                "name": "Evaluate string",
                "doc": "<TEST_STRING>",
                "obj": "Hello World!",
            },
            {
                "name": "Evaluate int",
                "doc": "<TEST_INT>",
                "obj": 456,
            },
            {
                "name": "Evaluate real",
                "doc": "<TEST_REAL>",
                "obj": 7.89,
            },
            {
                "name": "Evaluate boolean",
                "doc": "<TEST_BOOLEAN>",
                "obj": True,
            },
            {
                "name": "Evaluate null",
                "doc": "<TEST_NULL>",
                "obj": None,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_macro_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECMacro`` as its element.
        """
        test_cases = [
            {
                "name": "No macro with that name",
                "doc": "<TEST_UNKNOWN>",
                "obj": 0,
                "want": "At location $ - failed to find the JSPEC macro '<TEST_UNKNOWN>'",
            },
            {
                "name": "Not a JSON macro",
                "doc": "<TEST_BAD>",
                "obj": "bad_element",
                "want": "At location $ - failed to parse the JSPEC macro '<TEST_BAD>' as a JSON element",
            },
            {
                "name": "Not a JSON macro",
                "doc": "<TEST_OBJECT>",
                "obj": {"goodbye": "world"},
                "want": "At location $ - JSPEC macro '<TEST_OBJECT>' failed to match '{\"goodbye\": \"world\"}'",
            },
        ]
        self._bad_match(test_cases)