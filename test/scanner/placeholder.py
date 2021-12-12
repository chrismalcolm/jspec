"""JSPEC Testing Module for scanning JSPEC documents for a placeholder.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC,
    JSPECObjectPlaceholder,
    JSPECArrayPlaceholder,
    JSPECStringPlaceholder,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECBooleanPlaceholder,
    JSPECNumberPlaceholder,
    JSPECInequalityLessThan,
    JSPECInequalityLessThanOrEqualTo,
    JSPECInequalityMoreThan,
    JSPECInequalityMoreThanOrEqualTo,
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
                    JSPECObjectPlaceholder(),
                )
            },
            {
                "name": "Array placeholder",
                "doc": 'array',
                "want": JSPEC(
                    JSPECArrayPlaceholder(),
                )
            },
            {
                "name": "String placeholder",
                "doc": 'string',
                "want": JSPEC(
                    JSPECStringPlaceholder(),
                )
            },
            {
                "name": "Int placeholder",
                "doc": 'int',
                "want": JSPEC(
                    JSPECIntPlaceholder(None),
                )
            },
            {
                "name": "Int placeholder inequality (1)",
                "doc": 'int < 2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality (2)",
                "doc": 'int <= 4.5',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 4.5),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality (3)",
                "doc": 'int > -2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityMoreThan(), -2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality (4)",
                "doc": 'int >= -4.5e-10',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityMoreThanOrEqualTo(), -4.5e-10),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (1)",
                "doc": 'int< 2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (2)",
                "doc": 'int <2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (3)",
                "doc": 'int<2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (1)",
                "doc": 'int<= 2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (2)",
                "doc": 'int <=2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 2),
                    ),
                )
            },
            {
                "name": "Int placeholder inequality spacing (3)",
                "doc": 'int<=2',
                "want": JSPEC(
                    JSPECIntPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 2),
                    ),
                )
            },
            {
                "name": "Real placeholder",
                "doc": 'real',
                "want": JSPEC(
                    JSPECRealPlaceholder(None),
                )
            },
            {
                "name": "Real placeholder inequality (1)",
                "doc": 'real < 2',
                "want": JSPEC(
                    JSPECRealPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Real placeholder inequality (2)",
                "doc": 'real <= 4.5',
                "want": JSPEC(
                    JSPECRealPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 4.5),
                    ),
                )
            },
            {
                "name": "Real placeholder inequality (3)",
                "doc": 'real > -2',
                "want": JSPEC(
                    JSPECRealPlaceholder(
                        (JSPECInequalityMoreThan(), -2),
                    ),
                )
            },
            {
                "name": "Real placeholder inequality (4)",
                "doc": 'real >= -4.5e-10',
                "want": JSPEC(
                    JSPECRealPlaceholder(
                        (JSPECInequalityMoreThanOrEqualTo(), -4.5e-10),
                    ),
                )
            },
            {
                "name": "Boolean placeholder",
                "doc": 'bool',
                "want": JSPEC(
                    JSPECBooleanPlaceholder(),
                )
            },
            {
                "name": "Number placeholder",
                "doc": 'number',
                "want": JSPEC(
                    JSPECNumberPlaceholder(None),
                )
            },
            {
                "name": "Number placeholder inequality (1)",
                "doc": 'number < 2',
                "want": JSPEC(
                    JSPECNumberPlaceholder(
                        (JSPECInequalityLessThan(), 2),
                    ),
                )
            },
            {
                "name": "Number placeholder inequality (2)",
                "doc": 'number <= 4.5',
                "want": JSPEC(
                    JSPECNumberPlaceholder(
                        (JSPECInequalityLessThanOrEqualTo(), 4.5),
                    ),
                )
            },
            {
                "name": "Number placeholder inequality (3)",
                "doc": 'number > -2',
                "want": JSPEC(
                    JSPECNumberPlaceholder(
                        (JSPECInequalityMoreThan(), -2),
                    ),
                )
            },
            {
                "name": "Number placeholder inequality (4)",
                "doc": 'number >= -4.5e-10',
                "want": JSPEC(
                    JSPECNumberPlaceholder(
                        (JSPECInequalityMoreThanOrEqualTo(), -4.5e-10),
                    ),
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
                    JSPECObjectPlaceholder(),
                )
            },
            {
                "name": "Array placeholder not a string",
                "doc": '"array"',
                "notwant": JSPEC(
                    JSPECArrayPlaceholder(),
                )
            },
            {
                "name": "String placeholder not a string",
                "doc": '"string"',
                "notwant": JSPEC(
                    JSPECStringPlaceholder(),
                )
            },
            {
                "name": "Int placeholder",
                "doc": '"int"',
                "notwant": JSPEC(
                    JSPECIntPlaceholder(None),
                )
            },
            {
                "name": "Real placeholder",
                "doc": '"real"',
                "notwant": JSPEC(
                    JSPECRealPlaceholder(None),
                )
            },
            {
                "name": "Boolean placeholder",
                "doc": '"bool"',
                "notwant": JSPEC(
                    JSPECBooleanPlaceholder(),
                )
            },
            {
                "name": "Number placeholder",
                "doc": '"number"',
                "notwant": JSPEC(
                    JSPECNumberPlaceholder(None),
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_placeholder_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a placeholder as its element.
        """
        test_cases = [
            {
                "name": "Int bad inequality",
                "doc": 'int <: 4',
                "errmsg": "Invalid number",
                "errpos": 5,
            },
            {
                "name": "Real bad inequality",
                "doc": 'real < X',
                "errmsg": "Invalid number",
                "errpos": 7,
            },
            {
                "name": "Number bad inequality",
                "doc": 'number < a',
                "errmsg": "Invalid number",
                "errpos": 9,
            },
        ]
        self._error_match(test_cases)