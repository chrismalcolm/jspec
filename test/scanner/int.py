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
        test_cases = [
            {
                "name": "Basic int",
                "doc": '3',
                "want": JSPEC(
                    JSPECInt(3),
                )
            },
            {
                "name": "Two digits",
                "doc": '51',
                "want": JSPEC(
                    JSPECInt(51),
                )
            },
            {
                "name": "Many digits",
                "doc": '1234567890',
                "want": JSPEC(
                    JSPECInt(1234567890),
                )
            },
            {
                "name": "Negative",
                "doc": '-238',
                "want": JSPEC(
                    JSPECInt(-238),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_int_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECInt`` as its element.
        """
        test_cases = [
             {
                "name": "Should be real",
                "doc": '54.0',
                "notwant": JSPEC(
                    JSPECInt(54),
                )
            },
            {
                "name": "Negative is not positive",
                "doc": '78',
                "notwant": JSPEC(
                    JSPECInt(-78),
                )
            },
            {
                "name": "Positive is not negative",
                "doc": '-78',
                "notwant": JSPEC(
                    JSPECInt(78),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_int_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECInt`` as its element.
        """
        test_cases = [
            {
                "name": "Leading zero",
                "doc": '05',
                "errmsg": "Extra data",
                "errpos": 1,
            },
            {
                "name": "Leading zeros",
                "doc": '00001234',
                "errmsg": "Extra data",
                "errpos": 1,
            },
            {
                "name": "Double negative",
                "doc": '--6723',
                "errmsg": "Invalid number",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)