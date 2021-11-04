import unittest
import jspec
from jspec.scanner import JSPECDecodeError

class JSPECTestScanner(unittest.TestCase):
    """Base Class for testing the behaviour of the ``jspec.scanner`` module.

    All unit tests classes for the  ``jspec.scanner`` module should inherit
    from this class and use the methods below to run different types of test
    cases.
    """

    def _good_match(self, test_cases):
        """Run test cases expecting a good match.

        Each test case contains a JSPEC document and an expected JSPEC
        output. The JSPEC document the a string to be interpreted as a JSPEC.
        The expected JSPEC output is a JSPEC instance which we expect the
        ``jspec.scanner.scan`` to generate from scanning the JSPEC document.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "doc": `JSPEC_Document_1`,
                        "want": `Expected_JSPEC_output 1`
                    },
                    {
                        "doc": `JSPEC_Document_2`,
                        "want": `Expected_JSPEC_output_2`
                    },
                    ...
                ]
                JSPEC_Document_X is the JSPEC document for test case X
                Expected_JSPEC_output_X is the output for test case X
        """
        for test_case in test_cases:
            doc, want = test_case["doc"], test_case["want"]
            got = jspec.scanner.scan(doc)
            self.assertEqual(
                want,
                got,
                msg="Unexpected bad match - want: %s, got: %s" %  (want, got),
            )
    
    def _bad_match(self, test_cases):
        """Run test cases expecting a bad match.

        Each test case contains a JSPEC document and an unexpected JSPEC
        output. The JSPEC document the a string to be interpreted as a JSPEC.
        The unexpected JSPEC output is a JSPEC instance which we DO NOT expect
        the ``jspec.scanner.scan`` to generate from scanning the JSPEC
        document.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "doc": `JSPEC_Document_1`,
                        "notwant": `Unexpected_JSPEC_output_1`
                    },
                    {
                        "doc": `JSPEC_Document_2`,
                        "notwant": `Unexpected_JSPEC_output_2`
                    },
                    ...
                ]
                JSPEC_Document_X is the JSPEC document for test case X
                Unexpected_JSPEC_output_X is not the output for test case X
        """
        for test_case in test_cases:
            doc, want = test_case["doc"], test_case["notwant"]
            got = jspec.scanner.scan(doc)
            self.assertNotEqual(
                got,
                want,
                msg="Unexpected good match - got: %s" % got,
            )

    def _error_match(self, test_cases):
        """Run test cases expecting an error to be raised.

        Each test case contains a JSPEC document, an error message and an error
        position. The JSPEC document the a string to be interpreted as a JSPEC.
        The error message is the errmsg of the JSPECDecodeError that is
        expected to be raised when applying the ``jspec.scanner.scan`` method
        on the JSPEC document, The error position is the corresponding pos of
        the JSPECDecodeError, as an integer.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "doc": `JSPEC_Document_1`,
                        "errmsg": `Expected_errmsg_1`,
                        "errpos": `Expected_pos_1`
                    },
                    {
                        "doc": `JSPEC_Document_2`,
                        "errmsg": `Expected_errmsg_2`,
                        "errpos": `Expected_pos_2`
                    },
                    ...
                ]
                JSPEC_Document_X is the JSPEC document for test case X
                Expected_errmsg_X is the expected err.errmsg for test case X
                Expected_errmsg_X is the expected err.pos for test case X
                Where err is the raised JSPECDecodeError
        """
        for test_case in test_cases:
            doc, errmsg, errpos = test_case["doc"], test_case["errmsg"], test_case["errpos"]
            err = JSPECDecodeError(errmsg, doc, errpos)
            exc = None
            try:
                jspec.scanner.scan(doc)
            except Exception as e:
                exc = e
            self.assertEqual(
                str(err),
                str(exc),
                msg="Expected an error to be raised - want: %s, got: %s" %  (err, exc),
            )