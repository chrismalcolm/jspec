"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerString``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECString,
)

class JSPECTestScannerString(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    strings.

    A valid JSPEC string is any sequence of characters enclosed inside a pair
    of double quotes.
    """

    def test_scanner_string_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECString`` as its element.
        """
        test_cases = [   
            {
                # Basic string
                "doc": '"field"',
                "want": JSPEC(
                    JSPECString("field")
                )
            },
            {
                # Uppercase string
                "doc": '"ABCD"',
                "want": JSPEC(
                    JSPECString("ABCD")
                )
            },
            {
                # Mixed case string
                "doc": '"AxByCzD"',
                "want": JSPEC(
                    JSPECString("AxByCzD")
                )
            },
            {
                # Digit string
                "doc": '"1234567890"',
                "want": JSPEC(
                    JSPECString("1234567890")
                )
            },
            {
                # Mixed characters
                "doc": '"_1AbC$@vW;{:[(<*...>)]}"',
                "want": JSPEC(
                    JSPECString("_1AbC$@vW;{:[(<*...>)]}")
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_string_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECString`` as its element.
        """
        test_cases = [
            {
                # Misspelled 
                "doc": '"field"',
                "notwant": JSPEC(
                    JSPECString("feld")
                )
            },
            {
                # Uppercase to lowercase
                "doc": '"ABCD"',
                "notwant": JSPEC(
                    JSPECString("abcd")
                )
            },
            {
                # Lowercase to uppercase
                "doc": '"wxyz"',
                "notwant": JSPEC(
                    JSPECString("WXYZ")
                )
            },
            {
                # Digits as a number
                "doc": '123',
                "notwant": JSPEC(
                    JSPECString("123")
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_string_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECString`` as its element.
        """
        test_cases = [
            {
                # Missing first double quote
                "doc": 'field"',
                "errmsg": "Expecting value",
                "errpos": 0,
            },
            {
                # Missing final double quote
                "doc": '"field',
                "errmsg": "Unterminated string",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)