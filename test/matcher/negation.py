"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherNull``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherNegation(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    negation.

    A JSPEC element will match a negation if it doesn't match the negated
    element.
    """

    def test_matcher_negation_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECNegation`` as its element.
        """
        test_cases = [
            {
                "name": "Not an given object (1)",
                "doc": '!{"a":3}',
                "obj": {"a": 5},
            },
            {
                "name": "Not an given object (2)",
                "doc": '!{"a":3}',
                "obj": ["a", 5],
            },
            {
                "name": "Not an given array (1)",
                "doc": '!["a", 3]',
                "obj": ["a", 5],
            },
            {
                "name": "Not an given array (2)",
                "doc": '!["a", 3]',
                "obj": {"a": 5},
            },
            {
                "name": "Not an given string",
                "doc": '!"dog"',
                "obj": "cat",
            },
            {
                "name": "Not an given int",
                "doc": '!5',
                "obj": -5,
            },
            {
                "name": "Not an given real",
                "doc": '!3.00',
                "obj": 3,
            },
            {
                "name": "Not an given bool",
                "doc": '!true',
                "obj": None,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_negation_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECNegation`` as its element.
        """
        test_cases = [
            {
                "name": "Not an given object (1)",
                "doc": '!{"a":3}',
                "obj": {"a": 3},
                "want": "At location $ - expected '!{\"a\": 3}', got '{\"a\": 3}'",
            },
            {
                "name": "Not an given array (1)",
                "doc": '!["a", 3]',
                "obj": ["a", 3],
                "want": "At location $ - expected '![\"a\", 3]', got '[\"a\", 3]'",
            },
            {
                "name": "Not an given string",
                "doc": '!"dog"',
                "obj": "dog",
                "want": "At location $ - expected '!\"dog\"', got '\"dog\"'",
            },
            {
                "name": "Not an given int",
                "doc": '!5',
                "obj": 5,
                "want": "At location $ - expected '!5', got '5'",
            },
            {
                "name": "Not an given real",
                "doc": '!3.0',
                "obj": 3.0,
                "want": "At location $ - expected '!3.0', got '3.0'",
            },
            {
                "name": "Not an given bool",
                "doc": '!true',
                "obj": True,
                "want": "At location $ - expected '!true', got 'true'",
            },
        ]
        self._bad_match(test_cases)