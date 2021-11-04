"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerObject``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECObject,
)

class JSPECTestScannerObject(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    objects.

    A valid JSPEC object is a collection of key-element pairs enclosed in curly
    parentheses.
    """

    def test_scanner_object_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECObject`` as its element.
        """
        test_cases = []
        self._good_match(test_cases)

    def test_scanner_object_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECObject`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_object_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECObject`` as its element.
        """
        test_cases = []
        self._error_match(test_cases)