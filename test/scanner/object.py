"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerObject``.
"""

from test.scanner import JSPECTestScanner
from jspec.entity import (
    JSPEC, 
    JSPECObject,
    JSPECObjectPair,
    JSPECString,
    JSPECStringPlaceholder,
)

class JSPECTestScannerObject(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    objects.

    A valid JSPEC object is a collection of key-element pairs enclosed in curly
    parentheses.
    """

    def test_scanner_object_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECObject`` as its element.
        """
        test_cases = [
            {
                "name": "Basic object",
                "doc": '{"key":"value"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key"), JSPECString("value"))
                        ),
                    }),
                )
            },
            {
                "name": "Basic object with placeholder",
                "doc": '{string:"value"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECStringPlaceholder(), JSPECString("value"))
                        ),
                    }),
                )
            },
            {
                "name": "Basic multiple pairs",
                "doc": '{"key1":"value1","key2":"value2","key3":"value3"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key1"), JSPECString("value1"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key2"), JSPECString("value2"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key3"), JSPECString("value3"))
                        ),
                    }),
                )
            },
            {
                "name": "Basic multiple pairs unordered",
                "doc": '{"key1":"value1","key2":"value2","key3":"value3"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key2"), JSPECString("value2"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key1"), JSPECString("value1"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key3"), JSPECString("value3"))
                        ),
                    }),
                )
            },
            {
                "name": "Space (1)",
                "doc": '{\t"key1":"value1",\t"key2":"value2"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key1"), JSPECString("value1"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key2"), JSPECString("value2"))
                        ),
                    }),
                )
            },
            {
                "name": "Space (2)",
                "doc": '{"key1": "value1", "key2": "value2"}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key1"), JSPECString("value1"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key2"), JSPECString("value2"))
                        ),
                    }),
                )
            },
            {
                "name": "Space (3)",
                "doc": '{\t"key1":\t"value1" \t ,"key2": \t"value2" \t }',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("key1"), JSPECString("value1"))
                        ),
                        JSPECObjectPair(
                            (JSPECString("key2"), JSPECString("value2"))
                        ),
                    }),
                )
            },
            {
                "name": "Empty object",
                "doc": '{}',
                "want": JSPEC(
                    JSPECObject(set()),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_object_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECObject`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_object_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECObject`` as its element.
        """
        test_cases = [
            {
                "name": "Unterminated object",
                "doc": '{"a":"b"',
                "errmsg": "Unterminated object",
                "errpos": 8,
            },
            {
                "name": "Expecting field",
                "doc": '{1:"b"}',
                "errmsg": "Expecting property name enclosed in double quotes as key in object pair",
                "errpos": 1,
            },
            {
                "name": "Expected colon",
                "doc": '{"a","b"}',
                "errmsg": "Expecting key-value delimiter ':' in object",
                "errpos": 4,
            },
            {
                "name": "Expected colon",
                "doc": '{"a":}',
                "errmsg": "Expecting JSPEC term as value in object pair",
                "errpos": 5,
            },
            {
                "name": "Repeated object key for pair",
                "doc": '{"a":"b","a":"b"}',
                "errmsg": "Repeated object key for pair in object",
                "errpos": 16,
            },
            {
                "name": "Unterminated object (1)",
                "doc": '{"a":"b"',
                "errmsg": "Unterminated object",
                "errpos": 8,
            },
            {
                "name": "Unterminated object (2)",
                "doc": '{"a":"b"]',
                "errmsg": "Expecting object pair delimiter ','",
                "errpos": 8,
            },
            {
                "name": "Unterminated object (3)",
                "doc": '{',
                "errmsg": "Unterminated object",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)