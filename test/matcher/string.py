"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherString``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECString,
)

class JSPECTestMatcherString(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    strings.

    A JSPEC string will match a string which matches the regex of the JSPEC
    string.
    """

    def test_matcher_string_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECString`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_string_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECString`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)