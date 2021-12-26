"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerWildcard``.
"""

from test.scanner import JSPECTestScanner
from jspec.entity import (
    JSPEC,
    JSPECObjectPair, 
    JSPECWildcard,
    JSPECArray,
    JSPECInt,
    JSPECString,
    JSPECObject,
)

class JSPECTestScannerWildcard(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    wildcards.

    A valid JSPEC wildcard is a collection of elements enclosed in round
    brackets, with the elements separated by "|".
    """

    def test_scanner_wildcard_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECWildcard`` as its element.
        """
        test_cases = [
            {
                "name":"Basic wildcard",
                "doc": '*',
                "want": JSPEC(
                    JSPECWildcard()
                )
            },
            {
                "name":"Wildcard in array",
                "doc": '[*]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECWildcard(),
                    ])   
                )
            },
            {
                "name":"Double in array",
                "doc": '[*, *]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECWildcard(),
                        JSPECWildcard(),
                    ])   
                )
            },
            {
                "name":"Multiple wildcards in array",
                "doc": '[*, *, *, *]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECWildcard(),
                        JSPECWildcard(),
                        JSPECWildcard(),
                        JSPECWildcard(),
                    ])   
                )
            },
            {
                "name":"Mixed wildcards in array (1)",
                "doc": '[1, *, *, 5, *]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECWildcard(),
                        JSPECWildcard(),
                        JSPECInt(5),
                        JSPECWildcard(),
                    ])   
                )
            },
            {
                "name":"Mixed wildcards in array (2)",
                "doc": '[*, *, *, "hello"]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECWildcard(),
                        JSPECWildcard(),
                        JSPECWildcard(),
                        JSPECString("hello"),
                    ])   
                )
            },
            {
                "name":"Mixed wildcards in array (3)",
                "doc": '[{}, *, "blue"]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECObject(set()),
                        JSPECWildcard(),
                        JSPECString("blue"),
                    ])   
                )
            },
            {
                "name":"Mixed wildcards in array (4)",
                "doc": '[*, 3, "blue", *, 7, *]',
                "want": JSPEC(
                    JSPECArray([
                        JSPECWildcard(),
                        JSPECInt(3),
                        JSPECString("blue"),
                        JSPECWildcard(),
                        JSPECInt(7),
                        JSPECWildcard(),
                    ])   
                )
            },
            {
                "name":"Wildcard as value",
                "doc": '{"a": *}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair(
                            (JSPECString("a"), JSPECWildcard())
                        )
                    }),
                )
            },
             {
                "name":"Multiple Wildcard as value",
                "doc": '{"a": *, "b": *, "c": *}',
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair((JSPECString("a"), JSPECWildcard())),
                        JSPECObjectPair((JSPECString("b"), JSPECWildcard())),
                        JSPECObjectPair((JSPECString("c"), JSPECWildcard())),
                    }),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_wildcard_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECWildcard`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)

    def test_scanner_wildcard_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECWildcard`` as its element.
        """
        test_cases = [
            {
                "name":"Invlaid double wildcard",
                "doc": '**',
                "errmsg": "Extra data",
                "errpos": 1,
            },
              {
                "name":"Invlaid double wildcard in array",
                "doc": '[**]',
                "errmsg": "Expecting JSPEC term in array",
                "errpos": 2,
            },
            {
                "name":"Invlaid wildcard use in object as pair",
                "doc": '{*}',
                "errmsg": "Expecting property name enclosed in double quotes as key in object pair",
                "errpos": 1,
            },
            {
                "name":"Invlaid wildcard use in object as field",
                "doc": '{*: 1}',
                "errmsg": "Expecting property name enclosed in double quotes as key in object pair",
                "errpos": 1,
            },
            {
                "name":"Invlaid wildcard use in object as field and value",
                "doc": '{*: *}',
                "errmsg": "Expecting property name enclosed in double quotes as key in object pair",
                "errpos": 1,
            },
        ]
        self._error_match(test_cases)