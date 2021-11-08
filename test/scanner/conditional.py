"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerConditional``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECConditional,
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
)

class JSPECTestScannerConditional(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    conditionals.

    A valid JSPEC conditional is a collection of elements enclosed in round
    parentheses, with the elements separated by "|".
    """

    def test_scanner_conditional_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECConditional`` as its element.
        """
        test_cases = [
            {
                "name": "One element",
                "doc": '(1)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                    }),
                )
            },
            {
                "name": "Two elements",
                "doc": '(1|3)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(3),
                    }),
                )
            },
            {
                "name": "Multiple elements",
                "doc": '("a"|"b"|5|7.8|true|"c")',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(5),
                        JSPECReal(7.8),
                        JSPECBoolean(True),
                        JSPECString("c"),
                    }),
                )
            },
            {
                "name": "Embedded once",
                "doc": '(1|2|(3|4)|5)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECConditional({
                            JSPECInt(3),
                            JSPECInt(4),
                        }),
                        JSPECInt(5),
                    }),
                )
            },
            {
                "name": "Embedded multiple",
                "doc": '(((((true|false)))))',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECConditional({
                            JSPECConditional({
                                JSPECConditional({
                                    JSPECConditional({
                                        JSPECBoolean(True),
                                        JSPECBoolean(False),
                                    }),
                                }),
                            }),
                        }),
                    }),
                )
            },
            {
                "name": "Different order two",
                "doc": '(1|3)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(3),
                        JSPECInt(1),
                    }),
                )
            },
            {
                "name": "Different oder multiple",
                "doc": '("a"|"b"|5|78|true|"c")',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECString("c"),
                        JSPECString("a"),
                        JSPECString("b"),
                        JSPECInt(78),
                        JSPECBoolean(True),
                        JSPECInt(5),
                    }),
                )
            },
            {
                "name": "Spaces (1)",
                "doc": '( 1|2|3|4)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(3),
                        JSPECInt(4),
                    }),
                )
            },
            {
                "name": "Spaces (2)",
                "doc": '(1|2|3|4 )',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(3),
                        JSPECInt(4),
                    }),
                )
            },
            {
                "name": "Spaces (3)",
                "doc": '(\t1|2|\t3\t|4\t)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(3),
                        JSPECInt(4),
                    }),
                )
            },
            {
                "name": "Spaces (4)",
                "doc": '(1 | 2 | 3 | 4)',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(3),
                        JSPECInt(4),
                    }),
                )
            },
            {
                "name": "Spaces (5)",
                "doc": '( 1 | 2 | 3 | 4 )',
                "want": JSPEC(
                    JSPECConditional({
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(3),
                        JSPECInt(4),
                    }),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_conditional_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECConditional`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_conditional_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECConditional`` as its element.
        """
        test_cases = [
            {
                "name": "Empty conditional",
                "doc": '()',
                "errmsg": "Empty conditional",
                "errpos": 1,
            },
            {
                "name": "Unfinished conditional",
                "doc": '(1|)',
                "errmsg": "Expecting element in conditional",
                "errpos": 3,
            },
            {
                "name": "Unfinished conditional",
                "doc": '(1|2]',
                "errmsg": "Expecting conditional termination",
                "errpos": 4,
            },
        ]
        self._error_match(test_cases)