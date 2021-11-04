"""JSPEC Testing Module for matching JSPEC documents for a placeholder.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
)

class JSPECTestMatcherPlaceholder(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    placeholders.

    A valid JSPEC placeholder one of array, boolean, int, null, object, real or
    string.
    """

    def test_matcher_placeholder_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        placeholder as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_placeholder_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified placeholder as its element.
        """
        test_cases = []
        self._bad_match(test_cases)