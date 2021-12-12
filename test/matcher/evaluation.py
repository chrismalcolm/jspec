"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherEvaluation``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherEvaluation(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    evaluations.

    A JSPEC evaluation will match a evaluation.
    """

    def test_matcher_evaluation_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECEvaluation`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_evaluation_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECEvaluation`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)