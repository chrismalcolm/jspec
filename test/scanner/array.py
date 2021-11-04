"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerArray``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECArray,
)

class JSPECTestScannerArray(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    arrays.

    A valid JSPEC array is a collection of elements enclosed in square
    parentheses.
    """

    def test_scanner_array_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECArray`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_array_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECArray`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_array_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECArray`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)