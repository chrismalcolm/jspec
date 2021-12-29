"""JSPEC Testing Module for scanning JSPEC documents for comments.
"""

from test.scanner import JSPECTestScanner
from jspec.entity import (
    JSPEC, 
    JSPECNull,
    JSPECObject,
    JSPECObjectPair,
    JSPECString,
    JSPECArray,
    JSPECInt,
    JSPECObject,
    JSPECString,
)

class JSPECTestScannerComment(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    comments.

    A valid JSPEC comment is either the latter part of the line from double
    forward slashes '//' or a multiline comment, begining with a forward slash
    and asterisk '/*' and terminated by a asterisk and forward slash '*/'.
    """

    def test_scanner_comment_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a valid JSPEC.
        """
        test_cases = [
            {
                "name": "Single line comment, ending in newline",
                "doc": 'null// Some comment \n',
                "want": JSPEC(
                    JSPECNull(None),
                )
            },
            {
                "name": "Single line comment, ending in termination",
                "doc": 'null// Some comment',
                "want": JSPEC(
                    JSPECNull(None),
                )
            },
            {
                "name": "Multi-line comment on a single line (1)",
                "doc": """
                [
                    1,
                    2,
                    /* 3, */
                    4,
                    5
                ]
                """,
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(4),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Multi-line comment on a single line (2)",
                "doc": """
                [
                    1,
                    2,
                    /*/* 3, */
                    4,
                    5
                ]
                """,
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(4),
                        JSPECInt(5),
                    ]),
                )
            },
            {
                "name": "Multi-line comment on a single line",
                "doc": """
                [
                    1,
                    2,
                    /*
                    3,
                    4,
                    5,
                    */
                    6,
                    7
                ]
                """,
                "want": JSPEC(
                    JSPECArray([
                        JSPECInt(1),
                        JSPECInt(2),
                        JSPECInt(6),
                        JSPECInt(7),
                    ]),
                )
            },
            {
                "name": "Single-line comment object",
                "doc": """
                {//Okay
                    "a": 1
                }
                """,
                "want": JSPEC(
                    JSPECObject({
                        JSPECObjectPair((JSPECString("a"), JSPECInt(1)))
                    }),
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_null_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC``.
        """
        test_cases = [
            {
                "name": "Unterminated comment (1)",
                "doc": '[1,2 /*]',
                "errmsg": "Unterminated comment",
                "errpos": 5,
            },
            {
                "name": "Unterminated comment (2)",
                "doc": '[1,2/*]',
                "errmsg": "Unterminated comment",
                "errpos": 4,
            },
            {
                "name": "Double termination (1)",
                "doc": '[1,2/*  */*/]',
                "errmsg": "Expecting JSPEC term in array",
                "errpos": 10,
            },
            {
                "name": "Double termination (2)",
                "doc": '[1,2/*/*  */*/]',
                "errmsg": "Expecting JSPEC term in array",
                "errpos": 12,
            },
            {
                "name": "Double termination (3)",
                "doc": '[1,2  /*  */*/]',
                "errmsg": "Expecting JSPEC term in array",
                "errpos": 12,
            },
            {
                "name": "Double termination (4)",
                "doc": '[1,2   /*/*  */*/]',
                "errmsg": "Expecting JSPEC term in array",
                "errpos": 15,
            },
        ]
        self._error_match(test_cases)