"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerInt``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECInt,
)

class JSPECTestScannerInt(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    ints.

    A valid JSPEC int is a set of digits, with no leading zeroes, possibly
    preceded by a minus sign.
    """

    def test_scanner_int_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECInt`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_int_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECInt`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_int_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECInt`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)