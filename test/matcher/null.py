"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherNull``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherNull(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    nulls.

    A JSPEC null will match a null.
    """

    def test_matcher_null_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECNull`` as its element.
        """
        test_cases = [
            {
                "name": "Simple null",
                "doc": "null",
                "obj": None,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_null_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECNull`` as its element.
        """
        test_cases = [
            {
                "name": "Not null",
                "doc": "null",
                "obj": False,
                "want": "At location $ - expected 'None', got 'false'",
            },
        ]
        self._bad_match(test_cases)