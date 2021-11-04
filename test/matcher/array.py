"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherArray``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECArray,
)

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
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_array_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECArray`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)