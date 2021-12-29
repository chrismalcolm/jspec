import unittest
import jspec

class JSPECTestMatcher(unittest.TestCase):
    """Base Class for testing the behaviour of the ``jspec.matcher`` module.

    All unit tests classes for the  ``jspec.matcher`` module should inherit
    from this class and use the methods below to run different types of test
    cases.
    """

    def _good_match(self, test_cases):
        """Run test cases expecting a good match.

        Each test case contains a JSPEC document and an expected good match
        as a Python native JSON object. The JSPEC document is a string to be
        interpreted as a JSPEC. The expected bool output of the
        ``jspec.matcher.match`` is expected to be true.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "name": <TEST_NAME_1>,
                        "doc": <JSPEC_DOCUMENT_1>,
                        "obj": <PYTHON_JSON_OBJECT_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "doc": <JSPEC_DOCUMENT_2>,
                        "obj": <PYTHON_JSON_OBJECT_2>
                    },
                    ...
                ]
                where TEST_NAME_X is the name for the test case X,
                JSPEC_DOCUMENT_X is the JSPEC document for test case X and
                PYTHON_JSON_OBJECT_X is the Python native JSON object expected
                to be good match for for test case X.
        """
        for test_case in test_cases:
            name, doc, obj = test_case["name"], test_case["doc"], test_case["obj"]
            j = jspec.scanner.scan(doc)
            result, errormsg = jspec.matcher.match(j, obj)
            self.assertTrue(
                result,
                msg="(%s) Unexpected bad match: %s" % (name, errormsg),
            )
    
    def _bad_match(self, test_cases):
        """Run test cases expecting a bad match.

        Each test case contains a JSPEC document and an expected bad match
        as a Python native JSON object. The JSPEC document is a string to be
        interpreted as a JSPEC. The expected bool output of the
        ``jspec.matcher.match`` is expected to be false.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "name": <TEST_NAME_1>,
                        "doc": <JSPEC_DOCUMENT_1>,
                        "obj": <PYTHON_JSON_OBJECT_1>,
                        "want": <REASON_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "doc": <JSPEC_DOCUMENT_2>,
                        "obj": <PYTHON_JSON_OBJECT_2>,
                        "want": <REASON_2>
                    },
                    ...
                ]
                where TEST_NAME_X is the name for the test case X,
                JSPEC_DOCUMENT_X is the JSPEC document for test case X,
                PYTHON_JSON_OBJECT_X is the Python native JSON object expected
                to be bad match for for test case X and REASON_X is the reason
                the match failed.
        """
        for test_case in test_cases:
            name, doc, obj, want = test_case["name"], test_case["doc"], test_case["obj"], test_case["want"]
            j = jspec.scanner.scan(doc)
            result, got = jspec.matcher.match(j, obj)
            self.assertFalse(
                result,
                msg="(%s) Unexpected good match" % name,
            )
            self.assertEqual(
                want,
                got,
                msg="(%s) Expected a reason to be returned - want: %s, got: %s" %  (name, want, got),
            )

    def _error_match(self, test_cases):
        """Run test cases expecting an error to be raised.

        Each test case contains a JSPEC document, a JSPEC, a Python native JSON
        object and an error message. The ``jspec.matcher.match`` method will
        attempt to determine if the JSPEC and Python native JSON object is a
        match, and is expected to raise a Value Error with the given error
        message.

        Args:
            test_cases (list): The test cases, in the following format
                [
                    {
                        "name": <TEST_NAME_1>,
                        "spec": <JSPEC_1>,
                        "obj": <PYTHON_JSON_OBJECT_1>,
                        "errmsg": <ERROR_MESSAGE_1>
                    },
                    {
                        "name": <TEST_NAME_2>,
                        "spec": <JSPEC_2>,
                        "obj": <PYTHON_JSON_OBJECT_2>,
                        "errmsg": <ERROR_MESSAGE_2>
                    },
                    ...
                ]
                where TEST_NAME_X is the name for the test case X, JSPEC_X is
                the JSPEC instance for test case X, PYTHON_JSON_OBJECT_X is the
                Python native JSON object and ERROR_MESSAGE_X is the expected
                error message of the ValueError.
        """
        for test_case in test_cases:
            name, spec, obj, errmsg = test_case["name"], test_case["spec"], test_case["obj"], test_case["errmsg"]
            err = ValueError(errmsg)
            exc = None
            try:
                jspec.matcher.match(spec, obj)
            except Exception as e:
                exc = e
            self.assertEqual(
                str(err),
                str(exc),
                msg="(%s) Expected an error to be raised - want: %s, got: %s" %  (name, err, exc),
            )