"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerReal``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECReal,
    JSPECInt,
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
        test_cases = [
            {
                "name": "Basic real",
                "doc": '3.14',
                "want": JSPEC(
                    JSPECReal(3.14),
                )
            },
            {
                "name": "Exponent real with e",
                "doc": '1.234e6',
                "want": JSPEC(
                    JSPECReal(1.234e6),
                )
            },
             {
                "name": "Exponent real with e",
                "doc": '1.2345E6',
                "want": JSPEC(
                    JSPECReal(1.2345e6),
                )
            },
            {
                "name": "Exponent real with e",
                "doc": '1.234e6',
                "want": JSPEC(
                    JSPECReal(1.234e6),
                )
            },
            {
                "name": "Exponent vs value",
                "doc": '5.678e6',
                "want": JSPEC(
                    JSPECReal(5678000),
                )
            },
            {
                "name": "Exponent vs value",
                "doc": '7.77e7',
                "want": JSPEC(
                    JSPECReal(77700000),
                )
            },
            {
                "name": "No extra zero",
                "doc": '2.0',
                "want": JSPEC(
                    JSPECReal(2),
                )
            },
            {
                "name": "No extra zeroes",
                "doc": '4.0000000',
                "want": JSPEC(
                    JSPECReal(4),
                )
            },
            {
                "name": "Negative",
                "doc": '-3725.342',
                "want": JSPEC(
                    JSPECReal(-3725.342),
                )
            },
            {
                "name": "Negative with exponent",
                "doc": '-3725.342e10',
                "want": JSPEC(
                    JSPECReal(-3725.342e10),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_real_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECReal`` as its element.
        """
        test_cases = [
            {
                "name": "Extra decimal",
                "doc": '3.14',
                "notwant": JSPEC(
                    JSPECReal(3.142),
                )
            },
            {
                "name": "Missing decimal",
                "doc": '3.14',
                "notwant": JSPEC(
                    JSPECReal(3.1),
                )
            },
            {
                "name": "Can be int",
                "doc": '2.0',
                "notwant": JSPEC(
                    JSPECInt(2),
                )
            },
            {
                "name": "Negative is not positive",
                "doc": '78.9',
                "notwant": JSPEC(
                    JSPECReal(-78.9),
                )
            },
            {
                "name": "Positive is not negative",
                "doc": '-78.9',
                "notwant": JSPEC(
                    JSPECReal(78.9),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_real_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECReal`` as its element.
        """
        test_cases = [
            {
                "name": "No digits after decimal",
                "doc": '2.',
                "errmsg": "Extra data",
                "errpos": 1,
            },
            {
                "name": "No digits after e",
                "doc": '45.2E',
                "errmsg": "Extra data",
                "errpos": 4,
            },
            {
                "name": "No digits after e",
                "doc": '45.2e',
                "errmsg": "Extra data",
                "errpos": 4,
            },
            {
                "name": "Double negative",
                "doc": '--3.3',
                "errmsg": "Invalid number",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)