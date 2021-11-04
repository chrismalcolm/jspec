"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherObjectCaptureKey`` and
``JSPECTestMatcherObjectCaptureValue``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECObjectCaptureKey,
    JSPECObjectCaptureValue
)

class JSPECTestMatcherObjectCapture(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    object captures.

    A JSPEC object capture will match a set of key-element pairs, which all
    match at least one of the key-element pairs in the object capture.
    """

    def test_matcher_object_capture_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with
        ``JSPECTestMatcherObjectCaptureKey`` and
        ``JSPECTestMatcherObjectCaptureValue``.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_object_capture_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with
        ``JSPECTestMatcherObjectCaptureKey`` and
        ``JSPECTestMatcherObjectCaptureValue``.
        """
        test_cases = []
        self._bad_match(test_cases)