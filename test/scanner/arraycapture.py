"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerArrayCaptureElement``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC,
    JSPECArray,
    JSPECArrayCaptureElement,
    JSPECInt,
    JSPECWildcard,
)

class JSPECTestScannerArrayCapture(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    array captures.

    A valid JSPEC array capture is a collection of elements enclosed in angled
    parentheses, with the elements separated by "|".
    """

    def test_scanner_array_capture_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = [
            {
                "name": "Basic array capture",
                "doc": '[<1>]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }),
                    ]),
                )
            },
            {
                "name": "Array capture with elements",
                "doc": '[5,<1>,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }),
                        JSPECInt(4),
                    ]),
                )
            },
             {
                "name": "Basic array capture with multiplier",
                "doc": '[<1>x5]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }, multiplier=5),
                    ]),
                )
            },
            {
                "name": "Array capture with elements with multiplier",
                "doc": '[5,<1>x17,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }, multiplier=17),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Array ellipsis (1)",
                "doc": '[...]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECWildcard(None),
                        }),
                    ]),
                )
            },
            {
                "name": "Array ellipsis (2)",
                "doc": '[<*>]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECWildcard(None),
                        }),
                    ]),
                )
            },
            {
                "name": "Array ellipsis with elements",
                "doc": '[2 ,... ,6]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(2),
                        JSPECArrayCaptureElement({
                            JSPECWildcard(None),
                        }, is_ellipsis=True),
                        JSPECInt(6),
                    ]),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_array_capture_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with
        ``JSPECArrayCaptureElement``.
        """
        test_cases = [
            {
                "name": "Wrong value in capture (1)",
                "doc": '[<2>]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }),
                    ]),
                )
            },
            {
                "name": "Wrong value in capture (2)",
                "doc": '[1,<1>,1]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECArrayCaptureElement({
                            JSPECInt(2),
                        }),
                        JSPECInt(1),
                    ]),
                )
            },
            {
                "name": "Wrong multiplier",
                "doc": '[<1>x5]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }, multiplier=6),
                    ]),
                )
            },
            {
                "name": "No multiplier",
                "doc": '[5,<1>,4]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }, multiplier=17),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Unwanted multiplier",
                "doc": '[<1>x5]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureElement({
                            JSPECInt(1),
                        }),
                    ]),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_array_capture_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with ``JSPECArrayCaptureElement`.
        """
        test_cases = [
            {
                "name": "Redundant array capture",
                "doc": '[<1>,<1>]',
                "errmsg": "Redundant array capture",
                "errpos": 8,
            },
            {
                "name": "Empty capture",
                "doc": '[<>]',
                "errmsg": "Empty capture",
                "errpos": 2,
            },
            {
                "name": "Bad element in X",
                "doc": '[<X>]',
                "errmsg": "Expecting value in capture",
                "errpos": 2,
            },
            {
                "name": "Repeated element in capture conditional",
                "doc": '[<"abc"|"abc">]',
                "errmsg": "Repeated element in capture conditional",
                "errpos": 12,
            },
            {
                "name": "Expecting capture termination",
                "doc": '[<1)]',
                "errmsg": "Expecting capture termination",
                "errpos": 3,
            },
            {
                "name": "1 dot",
                "doc": '[.]',
                "errmsg": "Expecting ellipsis with 3 dots",
                "errpos": 1,
            },
            {
                "name": "2 dots",
                "doc": '[..]',
                "errmsg": "Expecting ellipsis with 3 dots",
                "errpos": 1,
            },
            {
                "name": "4 dots",
                "doc": '[....]',
                "errmsg": "Expecting ',' delimiter",
                "errpos": 4,
            },
        ]
        self._error_match(test_cases)