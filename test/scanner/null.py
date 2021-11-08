"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerNull``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECNull,
)

class JSPECTestScannerNull(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    nulls.

    A valid JSPEC null is the value "null".
    """

    def test_scanner_null_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECNull`` as its element.
        """
        test_cases = [
            {
                "name": "Basic null",
                "doc": 'null',
                "want": JSPEC(
                    JSPECNull(None),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_null_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECNull`` as its element.
        """
        test_cases = [
            {
                "name": "String null",
                "doc": '"null"',
                "notwant": JSPEC(
                    JSPECNull(None),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_null_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECNull`` as its element.
        """
        test_cases = [
            {
                "name": "Capital null",
                "doc": 'Null',
                "errmsg": "Expecting element",
                "errpos": 0,
            },
            {
                "name": "Python None",
                "doc": 'None',
                "errmsg": "Expecting element",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)