"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherReal``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECReal,
)

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
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_real_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECReal`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)