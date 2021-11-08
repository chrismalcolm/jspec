"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerObjectCaptureKey`` and
``JSPECTestScannerObjectCaptureValue``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECObject,
    JSPECObjectCaptureKey,
    JSPECObjectCaptureValue,
    JSPECString,
    JSPECWildcard,
    JSPECInt,
    JSPECNull,
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
                "name": "Basic object capture",
                "doc": '{<"a\d":"b">}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic object capture with paris",
                "doc": '{<"a\d":"b">,"c":"d"}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                        (
                            JSPECString("c"),
                            JSPECString("d"),
                        )
                    ]),
                )
            },
            {
                "name": "Basic object capture with multiplier",
                "doc": '{<"a\d":"b">x4}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }, multiplier=4),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }, multiplier=4),
                        ),
                    ]),
                )
            },
            {
                "name": "Basic object capture with paris with multiplier",
                "doc": '{<"a\d":"b">x20,"c":"d"}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }, multiplier=20),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }, multiplier=20),
                        ),
                        (
                            JSPECString("c"),
                            JSPECString("d"),
                        )
                    ]),
                )
            },
            {
                "name": "Object ellipsis (1)",
                "doc": '{...}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("", is_placeholder=True),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECWildcard(None),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Object ellipsis (2)",
                "doc": '{<string:*>}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("", is_placeholder=True),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECWildcard(None),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Object capture with paris and ellipsis (1)",
                "doc": '{<"a\d":"b">,"c":"d", ... }',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                        (
                            JSPECString("c"),
                            JSPECString("d"),
                        ),
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("", is_placeholder=True),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECWildcard(None),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Object capture with paris and ellipsis (1)",
                "doc": '{..., <"a\d":"b">,"c":"d"}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                        (
                            JSPECString("c"),
                            JSPECString("d"),
                        ),
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("", is_placeholder=True),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECWildcard(None),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Conditional (1)",
                "doc": '{<"a\d"|"c":"b">}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                                JSPECString("c"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Conditional (2)",
                "doc": '{<"a\d"|"c":"b"|4>}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                                JSPECString("c"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                                JSPECInt(4),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Conditional (3)",
                "doc": '{<"a\d":"b"|4>}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                                JSPECInt(4),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Conditional (2)",
                "doc": '{<"a\d"|"c"|"d"|"\w+":"b"|4|3|5|null>}',
                "want": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a\d"),
                                JSPECString("c"),
                                JSPECString("d"),
                                JSPECString("\w+"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                                JSPECInt(4),
                                JSPECInt(3),
                                JSPECInt(5),
                                JSPECNull(None),
                            }),
                        ),
                    ]),
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
                "doc": '{<"a":"b">}',
                "notwant": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("c"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("b"),
                            }),
                        ),
                    ]),
                )
            },
            {
                "name": "Wrong value",
                "doc": '{<"a":"b">}',
                "notwant": JSPEC(
                    JSPECObject([
                        (
                            JSPECObjectCaptureKey({
                                JSPECString("a"),
                            }),
                            JSPECObjectCaptureValue({
                                JSPECString("c"),
                            }),
                        ),
                    ]),
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
                "doc": '{<"a":"b">,<"a":"b">}',
                "errmsg": "Redundant object pair capture",
                "errpos": 20,
            },
            {
                "name": "Expecting property",
                "doc": '{<1:"b">}',
                "errmsg": "Expecting property name enclosed in double quotes in capture",
                "errpos": 2,
            },
            {
                "name": "Expecting conditional or colon (1)",
                "doc": '{<"a","b">}',
                "errmsg": "Expecting conditional operator or colon",
                "errpos": 5
            },
            {
                "name": "Expecting element value",
                "doc": '{<"a":X>}',
                "errmsg": "Expecting element value in capture",
                "errpos": 6
            },
            {
                "name": "Repeated key",
                "doc": '{<"a"|"a":1>}',
                "errmsg": "Repeated key in capture conditional",
                "errpos": 8
            },
            {
                "name": "Repeated value",
                "doc": '{<"a":1|1>}',
                "errmsg": "Repeated value in capture conditional",
                "errpos": 8
            },
            {
                "name": "Expecting conditional operator or colon (2)",
                "doc": '{<"a":1}',
                "errmsg": "Expecting conditional operator or capture termination",
                "errpos": 7
            },
            {
                "name": "One dot",
                "doc": '{.}',
                "errmsg": "Expecting ellipsis with 3 dots",
                "errpos": 1
            },
            {
                "name": "Two dots",
                "doc": '{..}',
                "errmsg": "Expecting ellipsis with 3 dots",
                "errpos": 1
            },
            {
                "name": "Four dots",
                "doc": '{....}',
                "errmsg": "Expecting ',' delimiter",
                "errpos": 4
            },
        ]
        self._error_match(test_cases)