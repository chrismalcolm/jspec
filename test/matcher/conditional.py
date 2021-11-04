"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherConditional``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECConditional,
)

class JSPECTestMatcherConditional(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    conditionals.

    A JSPEC conditional will match an element which matches any element in the
    conditional.
    """

    def test_matcher_conditional_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECConditional`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_conditional_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECConditional`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)