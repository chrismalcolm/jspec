"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerArray``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECArray,
    JSPECInt,
    JSPECString,
)

class JSPECTestScannerArray(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    arrays.

    A valid JSPEC array is a collection of elements enclosed in square
    parentheses.
    """

    def test_scanner_array_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECArray`` as its element.
        """
        test_cases = [
            {
                "name": "Basic array",
                "doc": '[1]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                    ]),
                )
            },
            {
                "name": "Two elements",
                "doc": '[1,2]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                    ]),
                )
            },
            {
                "name": "Multiple elements",
                "doc": '[1,2,"a","b",5]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Spaces (1)",
                "doc": '[\t1\t,\t2\t,\t"a"\t,\t"b"\t,\t5\t]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Spaces (2)",
                "doc": '[ 1,2,"a","b",5 ]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Spaces (3)",
                "doc": '[1, 2, "a", "b", 5]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Spaces (4)",
                "doc": '[ 1 , 2 , "a" , "b" , 5 ]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Spaces (5)",
                "doc": '[ \t1\t, 2\t,\t"a"\t,  "b"\t,\t5\t ]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Empty array",
                "doc": '[]',
                "want": JSPEC(
                    JSPECArray([]),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_array_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECArray`` as its element.
        """
        test_cases = [
            {
                "name": "Wrong order",
                "doc": '[2,1]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                    ]),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_array_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECArray`` as its element.
        """
        test_cases = [
            {
                "name": "Unterminated array",
                "doc": '[1,2',
                "errmsg": "Unterminated array",
                "errpos": 4,
            },
            {
                "name": "Unexpected characters",
                "doc": '[1,2,X]',
                "errmsg": "Expecting element",
                "errpos": 5,
            },
            {
                "name": "Ill terminated array",
                "doc": '[1,2)',
                "errmsg": "Expecting ',' delimiter",
                "errpos": 4,
            },
        ]
        self._error_match(test_cases)