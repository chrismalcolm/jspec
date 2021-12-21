"""JSPEC Testing Module for matching JSPEC documents errors.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECObject,
    JSPECArray,
    JSPECIntPlaceholder,
    JSPECRealPlaceholder,
    JSPECNumberPlaceholder,
)

class JSPECTestMatcherError(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    getting errors.
    """

    def test_matcher_error(self):
        """Test examples of good matches.
        The ``match`` method should return a ``ValueError``.
        """
        test_cases = [
            {
                "name": "Integer placeholder invalid inequalities",
                "spec": JSPEC(
                    JSPECIntPlaceholder(
                        (set(), 0),
                    ),
                ),
                "obj": 1,
                "errmsg": "JSPEC does not support inequalities of class <class 'set'>",
            },
            {
                "name": "Real placeholder invalid inequalities",
                "spec": JSPEC(
                    JSPECRealPlaceholder(
                        (set(), 0.0),
                    ),
                ),
                "obj": 1.1,
                "errmsg": "JSPEC does not support inequalities of class <class 'set'>",
            },
            {
                "name": "Number placeholder invalid inequalities",
                "spec": JSPEC(
                    JSPECNumberPlaceholder(
                        (set(), 0.0),
                    ),
                ),
                "obj": 1.1,
                "errmsg": "JSPEC does not support inequalities of class <class 'set'>",
            },
            {
                "name": "Object invalid pair",
                "spec": JSPEC(
                    JSPECObject({
                        int(),
                    }),
                ),
                "obj": dict(),
                "errmsg": "JSPEC objects do not support object paris of class <class 'int'>",
            },
            {
                "name": "Array invalid pair",
                "spec": JSPEC(
                    JSPECArray([
                        set(),
                    ]),
                ),
                "obj": list(),
                "errmsg": "JSPEC arrays do not support elements of class <class 'set'>",
            },
            {
                "name": "Array invalid pair",
                "spec": JSPEC(
                    set(),
                ),
                "obj": 1,
                "errmsg": "JSPEC do not support elements of class <class 'set'>",
            },
        ]
        self._error_match(test_cases)