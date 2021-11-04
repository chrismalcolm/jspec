"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherArrayCaptureElement``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECArrayCaptureElement,
)

class JSPECTestMatcherArrayCapture(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    array captures.

    A JSPEC array capture will match a consecutive set of elements, which all
    match at least one of the elements in the array capture.
    """

    def test_matcher_array_capture_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_array_capture_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = []
        self._bad_match(test_cases)