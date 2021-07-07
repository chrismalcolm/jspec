"""Test module for the JSPEC regex."""

import unittest
import jspec


class RegexTest(unittest.TestCase):
    """Class for testing JSPEC regex."""

    def test_regex_inside_array(self):
        """"Test good and bad examples of regex inside an array."""
        tests = [
            {
                "snippet": '["\w", "\d", "b", 2]',
                "good_matches": [
                    ["a", 1, "b", 2],
                    ["z", 9, "b", 2],
                ],
                "bad_matches": [
                    {"a": 1, "b": 2},
                    ["a", 1, "b", 3],
                    ["a", 44, "b", 2],
                    ["be", 8, "b", 2],
                    ["x", 1, "b", 3],
                    ["a", 1, "b", 2, "c", 3],
                ]
            }
        ]
        self._run(tests)

    def test_regex_inside_object(self):
        """"Test good and bad examples of regex inside an object."""
        tests = [
            {
                "snippet": '{"\w+": {"id-\d{4}": "green"}}',
                "good_matches": [
                    {"word": {"id-1256": "green"}},
                    {"other": {"id-3716": "green"}},
                ],
                "bad_matches": [
                    {"*not word*": {"id-1256": "green"}},
                    {"some": {"id-1256": "red"}},
                    {"some": {"id-1234567": "green"}},
                ]
            }
        ]
        self._run(tests)

    def test_regex_inside_nested(self):
        """"Test good and bad examples of regex inside nested arrays and objects."""
        tests = [
            {
                "snippet": '{"timestamp": ["\d+", "\d+"], "e-[A-Za-z]{6}": "\d"}',
                "good_matches": [
                    {"timestamp": [1200, 3600], "e-ArHqzL": 4},
                    {"timestamp": [1, 3], "e-aAzZAZ": 5},
                ],
                "bad_matches": [
                    {"timestamp": [1, 3, 4], "e-aAzZAZ": 5},
                    {"timestamps": [1, 3], "e-aAzZAZ": 5},
                    {"timestamp": [1, 3], "e-09asds": 5},
                    {"timestamp": [1, 3], "e-aAzZAZ": 55},
                ]
            }
        ]
        self._run(tests)  

    def _run(self, tests):
        for test in tests:
            snippet = test["snippet"]
            spec = jspec.loads(snippet)
            for good_match in test["good_matches"]:
                self.assertTrue(
                    spec.match(good_match).result(),
                    "Checking good match %s against %s" % (good_match, snippet)
                )
            for bad_match in test["bad_matches"]:
                self.assertFalse(
                    spec.match(bad_match).result(),
                    "Checking bad match %s against %s" % (bad_match, snippet)
                )