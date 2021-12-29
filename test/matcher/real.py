"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherReal``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherReal(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    reals.

    A JSPEC real will match a real of the same value.
    """

    def test_matcher_real_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECReal`` as its element.
        """
        test_cases = [
            {
                "name": "Simple real",
                "doc": "1.0",
                "obj": 1.0,
            },
            {
                "name": "Two decimals",
                "doc": "3.14",
                "obj": 3.14,
            },
            {
                "name": "Many decimals",
                "doc": "0.92384793291",
                "obj": 0.92384793291,
            },
            {
                "name": "Many zeros",
                "doc": "0.000000000000000007",
                "obj": 0.000000000000000007,
            },
            {
                "name": "Every digit",
                "doc": "0.123456789",
                "obj": 0.123456789,
            },
            {
                "name": "Negative",
                "doc": "-3.08",
                "obj": -3.08,
            },
            {
                "name": "Positive exponent",
                "doc": "2.7e10",
                "obj": 2.7e10,
            },
            {
                "name": "Negative exponent",
                "doc": "2.7e-10",
                "obj": 2.7e-10,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_real_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECReal`` as its element.
        """
        test_cases = [
            {
                "name": "Wrong value",
                "doc": "1.0",
                "obj": 0.1,
                "want": "At location $ - expected '1.0', got '0.1'",
            },
            {
                "name": "Wrong decimal",
                "doc": "3.14",
                "obj": 31.4,
                "want": "At location $ - expected '3.14', got '31.4'",
            },
            {
                "name": "Wrong zeros",
                "doc": "0.000000000000000007",
                "obj": 0.00000000000000007,
                "want": "At location $ - expected '7e-18', got '7e-17'",
            },
            {
                "name": "Negative not positive",
                "doc": "-3.08",
                "obj": 3.08,
                "want": "At location $ - expected '-3.08', got '3.08'",
            },
            {
                "name": "Positive not negative",
                "doc": "3.08",
                "obj": -3.08,
                "want": "At location $ - expected '3.08', got '-3.08'",
            },
            {
                "name": "Positive exponent not negative",
                "doc": "2.7e10",
                "obj": 2.7e-10,
                "want": "At location $ - expected '27000000000.0', got '2.7e-10'",
            },
            {
                "name": "Negative exponent not positive",
                "doc": "2.7e-10",
                "obj": 2.7e10,
                "want": "At location $ - expected '2.7e-10', got '27000000000.0'",
            },
        ]
        self._bad_match(test_cases)