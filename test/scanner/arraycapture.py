"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerArrayCaptureElement``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC,
    JSPECArray,
    JSPECArrayCaptureGroup,
    JSPECArrayEllipsis,
    JSPECInt,
    JSPECWildcard,
    JSPECNegation,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECArrayEllipsis,
    JSPECCaptureMultiplier,
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
        ``JSPECArrayCaptureGroup``.
        """
        test_cases = [
            {
                "name": "Basic array capture (1)",
                "doc": '[<1>x?]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture (2)",
                "doc": '[<1>x2]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(2, 2),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture (3)",
                "doc": '[<1>x?]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(None, None),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture (4)",
                "doc": '[<1>x2-?]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(2, None),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture (5)",
                "doc": '[<1>x?-4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(None, 4),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture (6)",
                "doc": '[<1>x3-5]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(3, 5),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic array capture with condition",
                "doc": '[<1 ^ 3>x?]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                                JSPECLogicalOperatorXor(),
                                JSPECInt(3),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                    ]),
                )
            },
            {
                "name": "Array capture with elements",
                "doc": '[5,<1>x?,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Array capture with elements and condition",
                "doc": '[5,<!1 & !2>x?,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECNegation(JSPECInt(1)),
                                JSPECLogicalOperatorAnd(),
                                JSPECNegation(JSPECInt(2)),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Basic array capture with multiplier",
                "doc": '[<1>x5]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(5, 5),
                        )
                    ]),
                )
            },
            {
                "name": "Array capture with elements with multiplier",
                "doc": '[5,<1>x17,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(17, 17),
                        ),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Array capture with elements with multiplier and condition",
                "doc": '[5,<1 | 2>x17,4]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                                JSPECLogicalOperatorOr(),
                                JSPECInt(2),
                            ],
                            JSPECCaptureMultiplier(17, 17),
                        ),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Array ellipsis (1)",
                "doc": '[...]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayEllipsis(),
                    ]),
                )
            },
            {
                "name": "Array ellipsis (2)",
                "doc": '[<*>x?]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECWildcard(),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                    ]),
                )
            },
            {
                "name": "Array ellipsis with elements",
                "doc": '[2 ,... ,6]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(2),
                        JSPECArrayEllipsis(),
                        JSPECInt(6),
                    ]),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_array_capture_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with
        ``JSPECArrayCaptureGroup``.
        """
        test_cases = [
            {
                "name": "Wrong value in capture (1)",
                "doc": '[<2>x?]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                    ]),
                )
            },
            {
                "name": "Wrong value in capture (2)",
                "doc": '[1,<1>x?,1]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(2),
                            ],
                            JSPECCaptureMultiplier(),
                        ),
                        JSPECInt(1),
                    ]),
                )
            },
            {
                "name": "Wrong multiplier",
                "doc": '[<1>x5]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ], 
                            JSPECCaptureMultiplier(6, 6),
                        ),
                    ]),
                )
            },
            {
                "name": "No multiplier",
                "doc": '[5,<1>x?,4]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECInt(5),
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier(17, 17)
                        ),
                        JSPECInt(4),
                    ]),
                )
            },
            {
                "name": "Unwanted multiplier",
                "doc": '[<1>x5]',
                "notwant": JSPEC(
                    JSPECArray([
                        JSPECArrayCaptureGroup(
                            [
                                JSPECInt(1),
                            ],
                            JSPECCaptureMultiplier()
                        ),
                    ]),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_array_capture_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with ``JSPECArrayCaptureGroup`.
        """
        test_cases = [
            {
                "name": "Redundant array capture",
                "doc": '[<1>x?,<1>x?]',
                "errmsg": "Redundant array capture",
                "errpos": 12,
            },
            {
                "name": "Empty capture",
                "doc": '[<>x?]',
                "errmsg": "Empty array capture",
                "errpos": 2,
            },
            {
                "name": "Bad element in X",
                "doc": '[<X>x?]',
                "errmsg": "Expecting element in array capture",
                "errpos": 2,
            },
            {
                "name": "No value after operator",
                "doc": '[<1&>x?]',
                "errmsg": "Expecting element in array capture",
                "errpos": 4,
            },
            {
                "name": "Expecting capture termination",
                "doc": '[<1)]',
                "errmsg": "Expecting array capture termination '>'",
                "errpos": 3,
            },
            {
                "name": "1 dot",
                "doc": '[.]',
                "errmsg": "Expecting array ellipsis with 3 dots '...'",
                "errpos": 1,
            },
            {
                "name": "2 dots",
                "doc": '[..]',
                "errmsg": "Expecting array ellipsis with 3 dots '...'",
                "errpos": 1,
            },
            {
                "name": "4 dots",
                "doc": '[....]',
                "errmsg": "Expecting element in array",
                "errpos": 4,
            },
             {
                "name": "Min > Max",
                "doc": '[<1>x5-4]',
                "errmsg": "Minimum for array capture multiplier is larger than the maximum",
                "errpos": 8,
            },
        ]
        self._error_match(test_cases)