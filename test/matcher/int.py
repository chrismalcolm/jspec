"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherInt``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECInt,
)

class JSPECTestMatcherInt(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    ints.

    A JSPEC int will match a int of the same value.
    """

    def test_matcher_int_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECInt`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_int_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECInt`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)