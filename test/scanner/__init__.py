import unittest
import jspec
from jspec.scanner import JSPECDecodeError

class JSPECTestScanner(unittest.TestCase):
    """Base Class for testing the behaviour of the ``jspec.scanner`` module.

    All unit tests classes for the ``jspec.scanner`` module should inherit
    from this class and use the methods below to run different types of test
    cases.
    """

    def _good_match(self, test_cases):
        """Run test cases expecting a good match.

        Each test case contains a JSPEC document and an expected JSPEC
        output. The JSPEC document is a string to be interpreted as a JSPEC.
        The expected JSPEC output is a JSPEC instance which we expect the
        ``jspec.scanner.scan`` to generate from scanning the JSPEC document.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "name": <TEST_NAME_1>,
                        "doc": <JSPEC_DOCUMENT_1>,
                        "want": <EXPECTED_JSPEC_OUTPUT_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "doc": <JSPEC_DOCUMENT_2>,
                        "want": <EXPECTED_JSPEC_OUTPUT_2>
                    },
                    ...
                ]
                where  TEST_NAME_X is the name for the test case X,
                JSPEC_DOCUMENT_X is the JSPEC document for test case X and 
                EXPECTED_JSPEC_OUTPUT_X is the expected output for test
                case X.
        """
        for test_case in test_cases:
            name, doc, want = test_case["name"], test_case["doc"], test_case["want"]
            got = jspec.scanner.scan(doc)
            self.assertEqual(
                want,
                got,
                msg="(%s) Unexpected bad match - want: %s, got: %s" %  (name, want, got),
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
                        "name": <TEST_NAME_1>,
                        "doc": <JSPEC_DOCUMENT_1>,
                        "notwant": <UNEXPECTED_JSPEC_OUTPUT_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "doc": <JSPEC_DOCUMENT_2>,
                        "notwant": <UNEXPECTED_JSPEC_OUTPUT_2>
                    },
                    ...
                ]
                where  TEST_NAME_X is the name for the test case X,
                JSPEC_DOCUMENT_X is the JSPEC document for test case X and 
                UNEXPECTED_JSPEC_OUTPUT_X is the unexpected output for test
                case X.
        """
        for test_case in test_cases:
            name, doc, want = test_case["name"], test_case["doc"], test_case["notwant"]
            got = jspec.scanner.scan(doc)
            self.assertNotEqual(
                got,
                want,
                msg="(%s) Unexpected good match - got: %s" % (name, got),
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
                        "name": <TEST_NAME_1>,
                        "doc": `JSPEC_DOCUMENT_1>,
                        "errmsg": `EXPECTED_ERRMSG_1>,
                        "errpos": `EXPECTED_POS_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "doc": <JSPEC_DOCUMENT_2>,
                        "errmsg": <EXPECTED_ERRMSG_2>,
                        "errpos": <EXPECTED_POS_2>
                    },
                    ...
                ]
                where  TEST_NAME_X is the name for the test case X, 
                JSPEC_DOCUMENT_X is the JSPEC document for test case X,
                EXPECTED_ERRMSG_X is the expected err.errmsg for test case X
                and EXPECTED_POS is the expected err.pos for test case X, where
                err is the raised JSPECDecodeError.
        """
        for test_case in test_cases:
            name, doc, errmsg, errpos = test_case["name"], test_case["doc"], test_case["errmsg"], test_case["errpos"]
            err = JSPECDecodeError(errmsg, doc, errpos)
            exc = None
            try:
                jspec.scanner.scan(doc)
            except Exception as e:
                exc = e
            self.assertEqual(
                str(err),
                str(exc),
                msg="(%s) Expected an error to be raised - want: %s, got: %s" %  (name, err, exc),
            )