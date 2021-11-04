"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherBoolean``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECBoolean,
)

class JSPECTestMatcherBoolean(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    booleans.

    A JSPEC boolean will match a boolean of the same value.
    """

    def test_matcher_boolean_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECBoolean`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_boolean_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECBoolean`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)