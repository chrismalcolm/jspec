"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerMacro``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECMacro,
)

class JSPECTestScannerMacro(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    macros.

    A valid JSPEC macro is any sequence of characters enclosed inside a pair
    of angled parentheses.
    """

    def test_scanner_evaluation_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECMacro`` as its element.
        """
        test_cases = [   
            {
                "name": "Basic macro",
                "doc": '<field>',
                "want": JSPEC(
                    JSPECMacro("field")
                )
            },
            {
                "name": "Basic macro",
                "doc": '<OTHER>',
                "want": JSPEC(
                    JSPECMacro("OTHER")
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_evaluation_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECMacro`` as its element.
        """
        test_cases = [
            {
                "name": "Misspelled",
                "doc": '<HELLO>',
                "notwant": JSPEC(
                    JSPECMacro("<HELLO>")
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_evaluation_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECMacro`` as its element.
        """
        test_cases = [
            {
                "name": "Unterminated macro",
                "doc": '<VALUE',
                "errmsg": "Unterminated macro",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)