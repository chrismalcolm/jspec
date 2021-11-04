import unittest
import jspec

class JSPECTestMatcher(unittest.TestCase):
    """Class for testing the ``jspec.matcher`` module.
    """

    def _good_match(self, test_cases):
        for test_case in test_cases:
            doc, obj = test_case["doc"], test_case["obj"]
            j = jspec.matchner.match(doc)
            result, errormsg = jspec.matcher.match(j, obj)
            self.assertTrue(
                result,
                msg="Unexpected bad match: %s" %  errormsg,
            )
    
    def _bad_match(self, test_cases):
        for test_case in test_cases:
            doc, obj, want = test_case["doc"], test_case["obj"], test_case["want"]
            j = jspec.matchner.match(doc)
            result, got = jspec.matcher.match(j, obj)
            self.assertFalse(
                result,
                msg="Unexpected good match",
            )
            self.assertEqual(
                want,
                got,
                msg="Expected an error to be raised - want: %s, got: %s" %  (want, got),
            )