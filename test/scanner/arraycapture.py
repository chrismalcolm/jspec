"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerArrayCaptureElement``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECArrayCaptureElement,
)

class JSPECTestScannerArrayCapture(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    array captures.

    A valid JSPEC array capture is a collection of elements enclosed in angled
    parentheses, with the elements separated by "|".
    """

    def test_scanner_array_capture_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_array_capture_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_array_capture_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with ``JSPECArrayCaptureElement`.
        """
        test_cases = []
        self._error_match(test_cases)