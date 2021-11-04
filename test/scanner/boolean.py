"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerBoolean``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECBoolean,
)

class JSPECTestScannerBoolean(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    booleans.

    A valid JSPEC boolean is either true or false.
    """

    def test_scanner_boolean_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECBoolean`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_boolean_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECBoolean`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_boolean_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECBoolean`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)