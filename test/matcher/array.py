"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherArray``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherArray(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    arrays.

    A JSPEC array will match an array with matching elements.
    """

    def test_matcher_array_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECArray`` as its element.
        """
        test_cases = [
            {
                "name": "Empty array",
                "doc": "[]",
                "obj": [],
            },
            {
                "name": "Sample",
                "doc": "[1, 2, 3]",
                "obj": [1, 2, 3],
            },
            {
                "name": "Embedded",
                "doc": '[[[["a", "b", "c"]]]]',
                "obj": [[[["a", "b", "c"]]]],
            },
        ]
        self._good_match(test_cases)

    def test_matcher_array_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECArray`` as its element.
        """
        test_cases = [
            {
                "name": "Empty array not object",
                "doc": "[]",
                "obj": {},
                "want": "At location $ - expected an array",
            },
            {
                "name": "Incorrect values",
                "doc": "[1, 2, 3]",
                "obj": [4, 5, 6],
                "want": "At location $[0] - expected '1', got '4'",
            },
            {
                "name": "Wrong order",
                "doc": "[3, 1, 2]",
                "obj": [3, 2, 1],
                "want": "At location $[1] - expected '1', got '2'",
            },
            {
                "name": "Embedded incorrect (1)",
                "doc": '[[[["a", "b", "c"]]]]',
                "obj": [[["a", "b", "c"]]],
                "want": "At location $[0][0][0] - expected an array",
            },
            {
                "name": "Embedded incorrect (2)",
                "doc": '[["a", "b", "c"]]',
                "obj": [[["a", "b", "c"]]],
                "want": "At location $[0][0] - expected a string",
            },
        ]
        self._bad_match(test_cases)