"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherNull``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECNull,
)

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
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_null_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECNull`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)