"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerObjectCaptureKey`` and
``JSPECTestScannerObjectCaptureValue``.
"""

from test.scanner import JSPECTestScanner
from jspec.entity import (
    JSPEC,
    JSPECObjectPair,
    JSPECObject,
    JSPECObjectCaptureGroup,
    JSPECString,
    JSPECWildcard,
    JSPECInt,
    JSPECStringPlaceholder,
    JSPECObjectEllipsis,
    JSPECLogicalOperatorAnd,
    JSPECLogicalOperatorOr,
    JSPECLogicalOperatorXor,
    JSPECCaptureMultiplier,
)

class JSPECTestScannerObjectCapture(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    object captures.

    A valid JSPEC object capture is a collection of key-element pairs enclosed
    in angled parentheses, with the  key-element pairs separated by "|".
    """

    def test_scanner_object_capture_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with
        ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = [
            {
                "name": "Basic object capture without multiplier",
                "doc": '{("a\d":"b")}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(1, 1)),
                    }),
                )
            },
            {
                "name": "Basic object capture (1)",
                "doc": '{("a\d":"b")x?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier()),
                    }),
                )
            },
            {
                "name": "Basic object capture (2)",
                "doc": '{("a\d":"b")x2}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(2, 2)),
                    }),
                )
            },
            {
                "name": "Basic object capture (3)",
                "doc": '{("a\d":"b")x?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(None, None)),
                    }),
                )
            },
            {
                "name": "Basic object capture (4)",
                "doc": '{("a\d":"b")x2-?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(2, None)),
                    }),
                )
            },
            {
                "name": "Basic object capture (5)",
                "doc": '{("a\d":"b")x?-?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(None, None)),
                    }),
                )
            },
            {
                "name": "Basic object capture (6)",
                "doc": '{("a\d":"b")x?-4}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(None, 4)),
                    }),
                )
            },
            {
                "name": "Basic object capture (7)",
                "doc": '{("a\d":"b")x1-7}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier(1, 7)),
                    }),
                )
            },
            {
                "name": "Basic object capture with pairs",
                "doc": '{("a\d":"b")x?,"c":"d"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b"))
                            )
                        ], JSPECCaptureMultiplier()),
                        JSPECObjectPair(
                            (JSPECString("c"), JSPECString("d"))
                        )
                    }),
                )
            },
            {
                "name": "Basic object capture with multiplier",
                "doc": '{("a\d":"b")x4}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup(
                            [
                                JSPECObjectPair(
                                    (JSPECString("a\d"), JSPECString("b")),
                                )
                            ], JSPECCaptureMultiplier(4, 4)
                        )
                    }),
                )
            },
            {
                "name": "Basic object capture with pairs with multiplier",
                "doc": '{("a\d":"b")x20,"c":"d"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup(
                            [
                                JSPECObjectPair(
                                    (JSPECString("a\d"),JSPECString("b")),
                                )
                            ], JSPECCaptureMultiplier(20, 20)
                        ),
                        JSPECObjectPair(
                            (JSPECString("c"), JSPECString("d"))
                        )
                    }),
                )
            },
            {
                "name": "Object ellipsis (1)",
                "doc": '{...}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectEllipsis(),
                    }),
                )
            },
            {
                "name": "Object ellipsis (2)",
                "doc": '{(string:*)x?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECStringPlaceholder(), JSPECWildcard()),
                            )
                        ], JSPECCaptureMultiplier())
                    }),
                )
            },
            {
                "name": "Object capture with paris and ellipsis (1)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b")),
                            )
                        ], JSPECCaptureMultiplier()),
                        JSPECObjectPair(
                            (JSPECString("c"), JSPECString("d"))
                        ),
                        JSPECObjectEllipsis(),
                    }),
                )
            },
            {
                "name": "Object capture with paris and ellipsis (2)",
                "doc": '{..., ("a\d":"b")x?,"c":"d"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECString("b")),
                            )
                        ], JSPECCaptureMultiplier()),
                        JSPECObjectPair(
                            (JSPECString("c"), JSPECString("d")),
                        ),
                        JSPECObjectEllipsis(),
                    }),
                )
            },
            {
                "name": "Object capture with logical operators (1)",
                "doc": '{("a\d":1 & "b\d":2)x?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECInt(1)),
                            ),
                            JSPECLogicalOperatorAnd(),
                            JSPECObjectPair(
                                (JSPECString("b\d"), JSPECInt(2)),
                            ),
                        ], JSPECCaptureMultiplier()),
                    }),
                )
            },
            {
                "name": "Object capture with logical operators (2)",
                "doc": '{("a\d":1 ^ "b\d":2 | "c\d":3)x?}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a\d"), JSPECInt(1)),
                            ),
                            JSPECLogicalOperatorXor(),
                            JSPECObjectPair(
                                (JSPECString("b\d"), JSPECInt(2)),
                            ),
                            JSPECLogicalOperatorOr(),
                            JSPECObjectPair(
                                (JSPECString("c\d"), JSPECInt(3)),
                            ),
                        ], JSPECCaptureMultiplier()),
                    }),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_object_capture_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with
        ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = [
            {
                "name": "Wrong key",
                "doc": '{("a":"b")x?}',
                "notwant": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("c"),JSPECString("b"))
                            ),
                        ], JSPECCaptureMultiplier()),
                    }),
                )
            },
            {
                "name": "Wrong value",
                "doc": '{("a":"b")x?}',
                "notwant": JSPEC(
                    JSPECObject({
                        JSPECObjectCaptureGroup([
                            JSPECObjectPair(
                                (JSPECString("a"),JSPECString("c"))
                            ),
                        ], JSPECCaptureMultiplier()),
                    }),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_object_capture_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with ``JSPECTestScannerObjectCaptureKey`` and
        ``JSPECTestScannerObjectCaptureValue``.
        """
        test_cases = [
            {
                "name": "Redundant object pair capture",
                "doc": '{("a":"b")x?,("a":"b")x?}',
                "errmsg": "Redundant object pair capture",
                "errpos": 24,
            },
            {
                "name": "Redundant object pair capture",
                "doc": '{("a":"b" | "c": 4)x?,("a":"b" | "c": 4)x?}',
                "errmsg": "Redundant object pair capture",
                "errpos": 42,
            },
            {
                "name": "Expecting property",
                "doc": '{(1:"b")x?}',
                "errmsg": "Expecting property name enclosed in double quotes as key in object capture pair",
                "errpos": 2,
            },
            {
                "name": "Expecting conditional or colon",
                "doc": '{("a","b")x?}',
                "errmsg": "Expecting key-value delimiter ':' in object capture",
                "errpos": 5
            },
            {
                "name": "Expecting element value",
                "doc": '{("a":X)x?}',
                "errmsg": "Expecting element as value in object capture pair",
                "errpos": 6
            },
            {
                "name": "Expecting capture termination",
                "doc": '{("a": "b"}',
                "errmsg": "Expecting object capture termination ')'",
                "errpos": 10
            },
            {
                "name": "One dot",
                "doc": '{.}',
                "errmsg": "Expecting object ellipsis with 3 dots '...'",
                "errpos": 1
            },
            {
                "name": "Two dots",
                "doc": '{..}',
                "errmsg": "Expecting object ellipsis with 3 dots '...'",
                "errpos": 1
            },
            {
                "name": "Four dots",
                "doc": '{....}',
                "errmsg": "Expecting object pair delimiter ','",
                "errpos": 4
            },
            {
                "name": "Double ellipsis",
                "doc": '{..., ...}',
                "errmsg": "Redundant object ellipsis",
                "errpos": 9
            },
            {
                "name": "Min ) Max",
                "doc": '{("a":1)x5-4}',
                "errmsg": "Minimum for object capture multiplier is larger than the maximum",
                "errpos": 12,    
            },
            {
                "name": "Empty capture",
                "doc": '{()x1-4}',
                "errmsg": "Empty object capture",
                "errpos": 2,    
            }
        ]
        self._error_match(test_cases)