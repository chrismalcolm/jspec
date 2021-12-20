"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherConditional``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherConditional(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    conditionals.

    A JSPEC conditional will match an element which matches any element in the
    conditional.
    """

    def test_matcher_conditional_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECConditional`` as its element.
        """
        test_cases = [
            {
                "name": "Single",
                "doc": "(bool)",
                "obj": False,
            },
            {
                "name": "Simple conditional (1)",
                "doc": "(object | array)",
                "obj": {},
            },
            {
                "name": "Simple conditional (2)",
                "doc": "(object | array)",
                "obj": [1, 2, 3, 4],
            },
            {
                "name": "Simple conditional (3)",
                "doc": "(int | 1.25 | null)",
                "obj": None,
            },
            {
                "name": "Simple conditional (4)",
                "doc": "(int | 1.25 | null)",
                "obj": 1.25,
            },
            {
                "name": "Simple conditional (5)",
                "doc": "(int | 1.25 | null)",
                "obj": 465,
            },
            {
                "name": "Simple conditional (6)",
                "doc": "(int > 5 & int < 7)",
                "obj": 6,
            },
            {
                "name": "Simple conditional (7)",
                "doc": "(int <= 5 ^ int >= 7)",
                "obj": 8,
            },
            {
                "name": "Embedded",
                "doc": "(((bool)))",
                "obj": True,
            },
            {
                "name": "Embedded multiple (1)",
                "doc": '(((bool | ("abc" | 123))))',
                "obj": True,
            },
            {
                "name": "Embedded multiple (2)",
                "doc": '(((bool | ("abc" | 123))))',
                "obj": "abc",
            },
            {
                "name": "Embedded multiple (3)",
                "doc": '(((bool | ("abc" | 123))))',
                "obj": 123,
            },
            {
                "name": "Embedded multiple (4)",
                "doc": '(((int < 7 & (int < 1 |int > 3))))',
                "obj": 4,
            },
        ]
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_conditional_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECConditional`` as its element.
        """
        test_cases = [
            {
                "name": "Single wrong",
                "doc": "(bool)",
                "obj": 1,
                "want": "At location $ - conditional elements ['bool'] do not match the element '1'",
            },
            {
                "name": "Multiple wrong",
                "doc": "(string | int | real)",
                "obj": ["a", 1, 1.1],
                "want": "At location $ - conditional elements ['int', 'real', 'string'] do not match the element '['a', 1, 1.1]'",
            },
            {
                "name": "Embedded wrong",
                "doc": "(string | int | (1.1 | 2.2 | 3.3))",
                "obj": ["a", 1, 1.1],
                "want": "At location $ - conditional elements ['(1.1 | 2.2 | 3.3)', 'int', 'string'] do not match the element '['a', 1, 1.1]'",
            },
        ]
        test_cases = []
        self._bad_match(test_cases)