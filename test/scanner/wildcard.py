"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerWildcard``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECWildcard,
)

class JSPECTestScannerWildcard(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    wildcards.

    A valid JSPEC wildcard is a collection of elements enclosed in round
    brackets, with the elements separated by "|".
    """

    def test_scanner_wildcard_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_wildcard_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_wildcard_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)