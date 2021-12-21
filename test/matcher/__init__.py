import unittest
import jspec

class JSPECTestMatcher(unittest.TestCase):
    """Class for testing the ``jspec.matcher`` module.
    """

    def _good_match(self, test_cases):
        for test_case in test_cases:
            name, doc, obj = test_case["name"], test_case["doc"], test_case["obj"]
            j = jspec.scanner.scan(doc)
            result, errormsg = jspec.matcher.match(j, obj)
            self.assertTrue(
                result,
                msg="(%s) Unexpected bad match: %s" % (name, errormsg),
            )
    
    def _bad_match(self, test_cases):
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
                msg="(%s) Expected an error to be raised - want: %s, got: %s" %  (name, want, got),
            )

    def _error_match(self, test_cases):
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