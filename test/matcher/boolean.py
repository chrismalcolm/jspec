"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherBoolean``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherBoolean(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    booleans.

    A JSPEC boolean will match a boolean of the same value.
    """

    def test_matcher_boolean_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECBoolean`` as its element.
        """
        test_cases = [
            {
                "name": "Simple boolean true",
                "doc": "true",
                "obj": True,
            },
            {
                "name": "Simple boolean false",
                "doc": "false",
                "obj": False,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_boolean_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECBoolean`` as its element.
        """
        test_cases = [
            {
                "name": "True not false",
                "doc": "false",
                "obj": True,
                "want": "At location $ - expected 'False', got 'true'",
            },
            {
                "name": "False not true",
                "doc": "true",
                "obj": False,
                "want": "At location $ - expected 'True', got 'false'",
            },
            {
                "name": "Int not boolean",
                "doc": "true",
                "obj": 1,
                "want": "At location $ - expected a boolean, got '1'",
            },
        ]
        self._bad_match(test_cases)