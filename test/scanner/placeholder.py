"""JSPEC Testing Module for scanning JSPEC documents for a placeholder.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC,
    JSPECObject,
    JSPECArray,
    JSPECString,
    JSPECInt,
    JSPECReal,
    JSPECBoolean,
)

class JSPECTestScannerPlaceholder(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    placeholders.

    A valid JSPEC placeholder one of array, boolean, int, null, object, real or
    string.
    """

    def test_scanner_placeholder_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        placeholder as its element.
        """
        test_cases = [
            {
                "name": "Object placeholder",
                "doc": 'object',
                "want": JSPEC(
                    JSPECObject([], is_placeholder=True),
                )
            },
            {
                "name": "Array placeholder",
                "doc": 'array',
                "want": JSPEC(
                    JSPECArray([], is_placeholder=True),
                )
            },
            {
                "name": "String placeholder",
                "doc": 'string',
                "want": JSPEC(
                    JSPECString("", is_placeholder=True),
                )
            },
            {
                "name": "Int placeholder",
                "doc": 'int',
                "want": JSPEC(
                    JSPECInt(0, is_placeholder=True),
                )
            },
            {
                "name": "Real placeholder",
                "doc": 'real',
                "want": JSPEC(
                    JSPECReal(0.0, is_placeholder=True),
                )
            },
            {
                "name": "Boolean placeholder",
                "doc": 'bool',
                "want": JSPEC(
                    JSPECBoolean(0.0, is_placeholder=True),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_placeholder_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified placeholder as its element.
        """
        test_cases = [
            {
                "name": "Object placeholder not a string",
                "doc": '"object"',
                "notwant": JSPEC(
                    JSPECObject([], is_placeholder=True),
                )
            },
            {
                "name": "Array placeholder not a string",
                "doc": '"array"',
                "notwant": JSPEC(
                    JSPECArray([], is_placeholder=True),
                )
            },
            {
                "name": "String placeholder not a string",
                "doc": '"string"',
                "notwant": JSPEC(
                    JSPECString("", is_placeholder=True),
                )
            },
            {
                "name": "Int placeholder",
                "doc": '"int"',
                "notwant": JSPEC(
                    JSPECInt(0, is_placeholder=True),
                )
            },
            {
                "name": "Real placeholder",
                "doc": '"real"',
                "notwant": JSPEC(
                    JSPECReal(0.0, is_placeholder=True),
                )
            },
            {
                "name": "Boolean placeholder",
                "doc": '"bool"',
                "notwant": JSPEC(
                    JSPECBoolean(0.0, is_placeholder=True),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_placeholder_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a placeholder as its element.
        """
        test_cases = []
        self._error_match(test_cases)