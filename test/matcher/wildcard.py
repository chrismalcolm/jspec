"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherWildcard``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECWildcard,
)

class JSPECTestMatcherWildcard(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    wildcards.

    A JSPEC wildcard will match any element.
    """

    def test_matcher_wildcard_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_wildcard_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)