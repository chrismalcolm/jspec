"""Test module for the JSPEC ellipsis template."""

import unittest
import jspec


class TemplateTest(unittest.TestCase):
    """Class for testing JSPEC ellipsis template."""

    def test_regex_inside_array(self):
        """"Test good and bad examples of ellipsis template inside an array."""
        tests = [
            {
                "snippet": '[ ... 1 ... ]',
                "good_matches": [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1],
                    []
                ],
                "bad_matches": [
                    [2],
                    [1, 1, 2],
                    [2, 1, 1, 1, 1, 1],
                    [1, 1, 3, 1, 1]
                ]
            },
            {
                "snippet": '[ ... "\w+" ... ]',
                "good_matches": [
                    ["red", "brick", "wall"],
                    ["s", "t"],
                    []
                ],
                "bad_matches": [
                    ["*red", "brick", "wall"],
                    ["s", "t", "?"],
                    ["!!!"]
                ]
            }
        ]
        self._run(tests)

    def test_regex_inside_object(self):
        """"Test good and bad examples of ellipsis template inside an object."""
        tests = [
            {
                "snippet": '{ ... "\w+": "\d+" ... }',
                "good_matches": [
                    {"a": 1, "b": 2, "y": 25, "z": 26},
                    {"red": 12, "blue": 67, "green": 44},
                ],
                "bad_matches": [
                    {"field": "not-digits"},
                    {"other": []},
                    {"last": 34, "field": "not-digits", "other": []},
                ]
            },
            {
                "snippet": '{ ... "\d": "okay" ... }',
                "good_matches": [
                    {"1": "okay", "2": "okay", "3": "okay"},
                    {"5": "okay", "4": "okay", "7": "okay"},
                ],
                "bad_matches": [
                    {"12": "okay", "2": "okay", "3": "okay"},
                    {"1": "okay", "2": "OKAY", "3": "okay"},
                ]
            }
        ]
        self._run(tests)

    def test_regex_inside_nested(self):
        """"Test good and bad examples of ellipsis template inside nested arrays and objects."""
        tests = [
            {
                "snippet": '{ ... "\w+": [ ... "\d" ... ] ... }',
                "good_matches": [
                    {"red": [1,2,3], "blue": [4]},
                    {"green": []},
                    {"a": [], "b": [1,2,3], "c": [4,5,6]}
                ],
                "bad_matches": [
                    {"word": [12, 13, 14], "other": "key-0af4", "extra": {}},
                    {"single": "not_a_array"},
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