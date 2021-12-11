"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerConditional``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECConditional,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECIntPlaceholder,
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
    JSPECNegation,
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
                    JSPECConditional([
                        JSPECInt(1),
                    ]),
                )
            },
            {
                "name": "Simple AND",
                "doc": '(int & !5)',
                "want": JSPEC(
                    JSPECConditional([
                        JSPECIntPlaceholder(),
                        JSPECLogicalOperatorAnd(),
                        JSPECNegation(JSPECInt(5)),
                    ]),
                )
            },
            {
                "name": "Simple OR",
                "doc": '(int | "hello")',
                "want": JSPEC(
                    JSPECConditional([
                        JSPECIntPlaceholder(),
                        JSPECLogicalOperatorOr(),
                        JSPECString("hello"),
                    ]),
                )
            },
            {
                "name": "Simple XOR",
                "doc": '(int ^ "hello")',
                "want": JSPEC(
                    JSPECConditional([
                        JSPECIntPlaceholder(),
                        JSPECLogicalOperatorXor(),
                        JSPECString("hello"),
                    ]),
                )
            },
            {
                "name": "Combination XOR",
                "doc": '(!int & !"hello" ^ "abc" | "okay")',
                "want": JSPEC(
                    JSPECConditional([
                        JSPECNegation(JSPECIntPlaceholder()),
                        JSPECLogicalOperatorAnd(),
                        JSPECNegation(JSPECString("hello")),
                        JSPECLogicalOperatorXor(),
                        JSPECString("abc"),
                        JSPECLogicalOperatorOr(),
                        JSPECString("okay"),
                    ]),
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
                "errmsg": "Expecting conditional termination ')'",
                "errpos": 4,
            },
        ]
        self._error_match(test_cases)