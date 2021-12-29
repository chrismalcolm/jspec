"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherInt``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherInt(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    ints.

    A JSPEC int will match a int of the same value.
    """

    def test_matcher_int_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECInt`` as its element.
        """
        test_cases = [
            {
                "name": "Simple integer",
                "doc": "1",
                "obj": 1,
            },
            {
                "name": "Two digits",
                "doc": "34",
                "obj": 34,
            },
            {
                "name": "Many digits",
                "doc": "92384793291",
                "obj": 92384793291,
            },
            {
                "name": "Every digit",
                "doc": "1234567890",
                "obj": 1234567890,
            },
            {
                "name": "Negative",
                "doc": "-308",
                "obj": -308,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_int_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECInt`` as its element.
        """
        test_cases = [
            {
                "name": "Incorrect value",
                "doc": "1",
                "obj": 2,
                "want": "At location $ - expected '1', got '2'",
            },
            {
                "name": "Positive not negative",
                "doc": "-45",
                "obj": 45,
                "want": "At location $ - expected '-45', got '45'",
            },
            {
                "name": "Negative not positive",
                "doc": "279",
                "obj": -279,
                "want": "At location $ - expected '279', got '-279'",
            },
        ]
        self._bad_match(test_cases)