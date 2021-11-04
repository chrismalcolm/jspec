"""JSPEC Testing Module for Scanner String.

This module tests the behaviour when using the ``match`` method for strings.
A valid JSPEC string is any sequence of characters enclosed inside a pair of
double quotes.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherObject(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``scan`` method for
    strings.
    """

    def test_scanner_string_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECString`` as its element.
        """
        test_cases = [   
            {
                # Basic string
                "doc": '{}',
                "obj": {}
            },
        ]
        self._good_match(test_cases)

    def test_scanner_string_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECString`` as its element.
        """
        test_cases = [
            {
                # Misspelled 
                "doc": '{}',
                "obj": [],
                "want": 'At location $ - expected an object',
            },
        ]
        self._bad_match(test_cases)