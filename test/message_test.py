"""Test module for the Result messages."""

import unittest
import jspec


class MessageTest(unittest.TestCase):
    """Class for testing Result message."""

    def test_messages(self):
        """"Test Result messages"""
        tests = [
            {    
                "snippet": '["\w", "\d", "b", 2]',
                "bad_match": {"a": 1, "b": 2},
                "message": "Unexpected JSON object at position '$'. Expected type: array"
            },
            {    
                "snippet": '{"\w+": {"id-\d{4}": "green"}}',
                "bad_match": {"*not word*": {"id-1256": "green"}},
                "message": "Cannot match key regex at position '$'. Want \w+. Got *not word*"
            },
            {    
                "snippet": '{"timestamp": ["\d+", "\d+"], "e-[A-Za-z]{6}": "\d"}',
                "bad_match": {"timestamp": [1, 3, 4], "e-aAzZAZ": 5},
                "message": "Mismatched array elements at position '$.timestamp'. Expected 2, got 3"
            },
            {    
                "snippet": '[1, 2, 3, ... ]',
                "bad_match": {"1": True, "2": True, "3": True},
                "message": "Unexpected JSON object at position '$'. Expected type: array"
            },
            {    
                "snippet": '{"a": 1, "b": 2, "c": 3, ... }',
                "bad_match": ["a", "b", "c"],
                "message": "Expected JSON object at position '$'"
            },
            {    
                "snippet": '[ ... 1 ... ]',
                "bad_match": [1, 1, 1, 1, 2],
                "message": "Template match failed: Cannot match regex at '$[4]'. 2 does not match 1"
            },
            {    
                "snippet": '{ ... "\w+": "\d+" ... }',
                "bad_match": {"field": "not-digits"},
                "message": "Cannot match regex at '$.field'. not-digits does not match \d+"
            },
            {    
                "snippet": '{ ... "\w+": [ ... "\d" ... ] ... }',
                "bad_match": {"word": [12, 13, 14], "other": "key-0af4", "extra": {}},
                "message": "Template match failed: Cannot match regex at '$.word[0]'. 12 does not match \d"
            }
        ]
        self._run(tests)

    def _run(self, tests):
        for test in tests:
            snippet = test["snippet"]
            bad_match = test["bad_match"]
            message = test["message"]
            spec = jspec.loads(snippet)
            #print(spec.match(bad_match).message())
            self.assertEqual(
                spec.match(bad_match).message(),
                message,
                "Checking for message equaling to %s for %s against %s" % (message, bad_match, snippet)
            )