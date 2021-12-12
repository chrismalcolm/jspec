"""JSPEC Testing Module for scanning JSPEC documents for
``JSPECTestScannerEvaluation``.
"""

from test.scanner import JSPECTestScanner
from jspec.component import (
    JSPEC, 
    JSPECEvaluation,
)

class JSPECTestScannerEvaluation(JSPECTestScanner):
    """Class for testing the behaviour when using the ``scan`` method for
    evaluations.

    A valid JSPEC evaluation is any sequence of characters enclosed inside a
    pair of angled parentheses.
    """

    def test_scanner_evaluation_good(self):
        """Test examples of good matches.
        The ``scan`` method should return a matching ``JSPEC`` with a
        ``JSPECEvaluation`` as its element.
        """
        test_cases = [   
            {
                "name": "Basic evaluation",
                "doc": '<field>',
                "want": JSPEC(
                    JSPECEvaluation("field")
                )
            },
            {
                "name": "Basic evaluation",
                "doc": '<1+2 * 89>',
                "want": JSPEC(
                    JSPECEvaluation("1+2 * 89")
                )
            },
        ]
        self._good_match(test_cases)

    def test_scanner_evaluation_bad(self):
        """Test examples of bad matches.
        The ``scan`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECEvaluation`` as its element.
        """
        test_cases = [
            {
                "name": "Misspelled",
                "doc": '<HELLO>',
                "notwant": JSPEC(
                    JSPECEvaluation("<HELLO>")
                )
            },
        ]
        self._bad_match(test_cases)

    def test_scanner_evaluation_error(self):
        """Test examples of error matches.
        The ``scan`` method should raise an error, associated with attempting
        to scan for a ``JSPEC`` with a ``JSPECEvaluation`` as its element.
        """
        test_cases = [
            {
                "name": "Unterminated evaluation",
                "doc": '<VALUE',
                "errmsg": "Unterminated evaluation",
                "errpos": 0,
            },
        ]
        self._error_match(test_cases)