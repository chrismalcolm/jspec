"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherNull``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherNegation(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    negation.

    A JSPEC element will match a negation if it doesn't match the negated
    element.
    """

    def test_matcher_negation_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECNegation`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_negation_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECNegation`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)