"""Test module for the JSPEC ellipsis substitution."""

import unittest
import jspec


class SubstitutionTest(unittest.TestCase):
    """Class for testing JSPEC ellipsis substitution."""

    def test_substitution_inside_array(self):
        """"Test good and bad examples of ellipsis substitution inside arrays."""
        tests = [
            {
                "snippet": '[1, 2, 3, ... ]',
                "good_matches": [
                    [1, 2, 3, 4, 5],
                    [1, 2, 3],
                    [1, 2, 3, {"h": "e"}]
                ],
                "bad_matches": [
                    {"1": True, "2": True, "3": True},
                    [1, 2, 4],
                    [1, 1, 2, 3],
                ]
            },
            {
                "snippet": '[ ... ,"d" ,"e"]',
                "good_matches": [
                    ["a", "b", "c", "d", "e"],
                    ["d", "e"],
                    [{"h": "e"}, "d", "e"],
                ],
                "bad_matches": [
                    {"d": True, "e": True},
                    ["a", "b", "d"],
                    ["a", "b", "c", "d", "e", "e"],
                ]
            },
            {
                "snippet": '[6, ... , 9, 10]',
                "good_matches": [
                    [6, 7, 8, 9, 10],
                    [6, 9, 10],
                    [6, 7, 8, 9, 10],
                    [6, 6, 6, 9, 10],
                ],
                "bad_matches": [
                    {"6": True, "9": True, "10": True},
                    [6, 9, "A", 10],
                    [6, 9, 9, 9, 10],
                ]
            },
            {
                "snippet": '[ ... ]',
                "good_matches": [
                    [],
                    ["a", "b", "c", "d", "e"],
                    [6, 7, 8, 9, 10],
                    [1, 2, 3, "x", "y", "z"],
                ],
                "bad_matches": [
                    {"6": True, "9": True, "10": True},
                    {},
                    {"side": "red"}
                ]
            }
        ]
        self._run(tests)  

    def test_substitution_inside_object(self):
        """"Test good and bad examples of ellipsis substitution inside objects."""
        tests = [
            {
                "snippet": '{"a": 1, "b": 2, "c": 3, ... }',
                "good_matches": [
                    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
                    {"a": 1, "b": 2, "c": 3},
                    {"a": 1, "b": 2, "c": 3, "d": {"h": "e"}},
                ],
                "bad_matches": [
                    ["a", "b", "c"],
                    {"a": 1, "b": 2, "d": 3},
                    {"a": 1, "b": 2, "c": 4},
                ]
            },
            {
                "snippet": '{ ...,  "y": 25, "z": 26}',
                "good_matches": [
                    {"v": 22, "w": 23, "x": 24, "y": 25, "z": 26},
                    {"y": 25, "z": 26},
                    {"y": 25, "z": 26, "s": {"h": "e"}},
                ],
                "bad_matches": [
                    ["a", "b", "c"],
                    {"y": 25, "a": 26},
                    {"v": 22, "w": 23, "x": 24, "y": 25, "z": 0},
                ]
            },
            {
                "snippet": '{ "a": 1,  "b": 2, ... ,"z": 26}',
                "good_matches": [
                    {"a": 1, "b": 2, "c": 3, "x": 24, "y": 25, "z": 26},
                    {"a": 1, "b": 2, "z": 26},
                    {"p": 44, "a": 1, "b": 2, "z": 26, "o": 5}
                ],
                "bad_matches": [
                    ["a", "b", "z"],
                    {"a": 1, "b": 2, "z": 0},
                    {"a": 1, "c": 2, "z": 26, "s": 5},
                ]
            },
            {
                "snippet": '{ ... }',
                "good_matches": [
                    {},
                    {"a": 1, "z": 26},
                    {"a": 1, "b": 2, "c": 3, "x": 24, "y": 25, "z": 26},
                ],
                "bad_matches": [
                    [],
                    [1, 2, 3],
                ]
            }
        ]
        self._run(tests) 

    def test_substitution_inside_nested(self):
        """"Test good and bad examples of ellipsis substitution inside nested arrays and objects."""
        tests = [
            {
                "snippet": '{"same_\w+": ["\d{2}", ... , 14], "other": "key-[0-9a-f]{4}", ...}',
                "good_matches": [
                    {"same_word": [12, 13, 14], "other": "key-0af4", "extra": {}},
                    {"same_word": [12, 13, 14], "other": "key-0af4", "extra": {}},
                    {"same_right": [10, 14], "other": "key-cccc"},
                ],
                "bad_matches": [
                    {"same_word": [12, 13, 14], "extra": {}},
                    {"other": "key-0af4", "extra": {}},
                    {"extra": {}},
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