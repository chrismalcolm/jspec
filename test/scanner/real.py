"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerReal``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECReal,
)

class JSPECTestScannerReal(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    reals.

    A valid JSPEC real is a set of digits, with no leading zeroes, possibly
    preceded by a minus sign, with an optional fractional part and an optional
    exponential part.
    """

    def test_scanner_real_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECReal`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_real_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECReal`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_real_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECReal`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)