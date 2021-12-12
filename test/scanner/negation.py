"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerNegation``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECNegation,
    JSPECObject,
    JSPECObjectPair,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
)

class JSPECTestScannerNegation(JSPECTestScanner):
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
                "name": "One element int",
                "doc": '!1',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECInt(1),
                    ),
                )
            },
            {
                "name": "One element string",
                "doc": '!"a"',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECString("a"),
                    ),
                )
            },
            {
                "name": "One element array",
                "doc": '!["a", "b", "c"]',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECArray([
                            JSPECString("a"),
                            JSPECString("b"),
                            JSPECString("c"),
                        ]),
                    ),
                )
            },
            {
                "name": "One element object",
                "doc": '!{"a": 1, "b": 2, "c": 3}',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECObject({
                            JSPECObjectPair((JSPECString("a"), JSPECInt(1))),
                            JSPECObjectPair((JSPECString("b"), JSPECInt(2))),
                            JSPECObjectPair((JSPECString("c"), JSPECInt(3))),
                        }),
                    ),
                )
            },
            {
                "name": "Double negation",
                "doc": '!!"s"',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECNegation(
                            JSPECString("s"),
                        ),
                    ),
                )
            },
            {
                "name": "Triple negation",
                "doc": '!!!"t"',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECNegation(
                            JSPECNegation(
                                JSPECString("t"),
                            ),
                        ),
                    ),
                )
            },
            {
                "name": "Multiple",
                "doc": '!!!!!"a"',
                "want": JSPEC(
                    JSPECNegation(
                        JSPECNegation(
                            JSPECNegation(
                                JSPECNegation(
                                    JSPECNegation(
                                        JSPECString("a"),
                                    ),
                                ),
                            ),
                        ),
                    ),
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
                "name": "No element in negation",
                "doc": '!',
                "errmsg": "Expecting element in negation",
                "errpos": 1,
            },
        ]
        self._error_match(test_cases)