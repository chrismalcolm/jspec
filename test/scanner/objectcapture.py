"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerObjectCaptureKey`` and
``JSPECTestScannerObjectCaptureValue``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECObjectCaptureKey,
    JSPECObjectCaptureValue
)

class JSPECTestScannerObjectCapture(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    object captures.

    A valid JSPEC object capture is a collection of key-element pairs enclosed
    in angled parentheses, with the  key-element pairs separated by "|".
    """

    def test_scanner_object_capture_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with
        ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_object_capture_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with
        ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_object_capture_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = []
        self._error_match(test_cases)