"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherObjectCaptureKey`` and
``JSPECTestMatcherObjectCaptureValue``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherObjectCapture(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    object captures.

    A JSPEC object capture will match a set of key-element pairs, which all
    match at least one of the key-element pairs in the object capture.
    """

    def test_matcher_object_capture_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with
        ``JSPECTestMatcherObjectCaptureKey`` and
        ``JSPECTestMatcherObjectCaptureValue``.
        """
        test_cases = [
            {
                "name": "Basic object capture without multiplier",
                "doc": '{("a\d":"b")}',
                "obj": {"a1": "b"},
            },
            {
                "name": "Basic object capture (0)",
                "doc": '{("a\d":"b")x?}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (1)",
                "doc": '{("a\d":"b")x?}',
                "obj": {},
            },
            {
                "name": "Basic object capture (2)",
                "doc": '{("a\d":"b")x2}',
                "obj": {"a1": "b", "a2": "b"},
            },
            {
                "name": "Basic object capture (3)",
                "doc": '{("a\d":"b")x2-?}',
                "obj": {"a1": "b", "a2": "b"},
            },
            {
                "name": "Basic object capture (4)",
                "doc": '{("a\d":"b")x2-?}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (5)",
                "doc": '{("a\d":"b")x?-?}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (6)",
                "doc": '{("a\d":"b")x?-?}',
                "obj": {},
            },
            {
                "name": "Basic object capture (7)",
                "doc": '{("a\d":"b")x?-4}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (8)",
                "doc": '{("a\d":"b")x?-4}',
                "obj": {},
            },
            {
                "name": "Basic object capture (9)",
                "doc": '{("a\d":"b")x?-3}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (10)",
                "doc": '{("a\d":"b")x1-7}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (11)",
                "doc": '{("a\d":"b")x1-3}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "Basic object capture (12)",
                "doc": '{("a\d":"b")x3-5}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
            },
            {
                "name": "asdad",
                "doc": '{("a1":"b")x1,("a\d":"b")x2,"c":"d"}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Basic object capture with pairs",
                "doc": '{("a\d":"b")x?,"c":"d"}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Object ellipsis (1.0)",
                "doc": '{...}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Object ellipsis (1.1)",
                "doc": '{...}',
                "obj": {},
            },
            {
                "name": "Object ellipsis (1.2)",
                "doc": '{..., "c": "d"}',
                "obj": {"c": "d"},
            },
            {
                "name": "Object ellipsis (1.2)",
                "doc": '{..., "c": "d"}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Object ellipsis (2.0)",
                "doc": '{(string:*)x?}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Object ellipsis (2.1)",
                "doc": '{(string:*)x?}',
                "obj": {},
            },
            {
                "name": "Object capture with paris and ellipsis (1)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d"},
            },
            {
                "name": "Object capture with paris and ellipsis (2)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d", "e": "f"},
            },
            {
                "name": "Object capture with paris and ellipsis (3)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "c": "d", "e": "f", "g": []},
            },
            {
                "name": "Object capture with paris and ellipsis (4)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "obj": {"c": "d"},
            },
            {
                "name": "Object capture with logical operators (1)",
                "doc": '{("\w2":1 & "b\d":1)x?}',
                "obj": {"b2": 1},
            },
            {
                "name": "Object capture with logical operators (2)",
                "doc": '{("\w2":1 & "b\d":1)x?}',
                "obj": {},
            },
            {
                "name": "Object capture with logical operators (3)",
                "doc": '{("a\d":1 ^ "b\d":2 | "c\d":3)x?}',
                "obj": {"c3": 3, "a3":1},
            },
        ]
        self._good_match(test_cases)

    def test_matcher_object_capture_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with
        ``JSPECTestMatcherObjectCaptureKey`` and
        ``JSPECTestMatcherObjectCaptureValue``.
        """
        test_cases = [
            {
                "name": "Basic object capture without multiplier",
                "doc": '{("a\d":"b")}',
                "obj": {"a1": "b1"},
                "want": "At location $ - failed object capture, '\"a1\": \"b1\"' failed to match '(\"a\d\": \"b\")x1'",
            },
            {
                "name": "Basic object capture (0)",
                "doc": '{("a\d":"b")x?}',
                "obj": {"a11": "b", "a21": "b", "a31": "b"},
                "want": 'At location $ - failed to match the following JSON pairs: ["a11": "b", "a21": "b", "a31": "b"]',
            },
            {
                "name": "Basic object capture (1)",
                "doc": '{("a\d":"b")x?}',
                "obj": {"a1": "b1"},
                "want": "At location $ - failed object capture, '\"a1\": \"b1\"' failed to match '(\"a\d\": \"b\")x?'",
            },
            {
                "name": "Basic object capture (1.1)",
                "doc": '{("a\d":"b")x?}',
                "obj": {"a1": "b", "a2": "b", "a3": "b", "a4": "b1"},
                "want": "At location $ - failed object capture, '\"a4\": \"b1\"' failed to match '(\"a\d\": \"b\")x?'",
            },
            {
                "name": "Basic object capture (2)",
                "doc": '{("a\d":"b")x2}',
                "obj": {"a1": "b"},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [(\"a\d\": \"b\")x2]",
            },
            {
                "name": "Basic object capture (3)",
                "doc": '{("a\d":"b")x2}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
                "want": "At location $ - failed to match the following JSON pairs: [\"a1\": \"b\", \"a2\": \"b\", \"a3\": \"b\"]",
            },
            {
                "name": "Basic object capture (4)",
                "doc": '{("a\d":"b")x2-?}',
                "obj": {"a1": "b"},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [(\"a\d\": \"b\")x2-?]",
            },
            {
                "name": "Basic object capture (5)",
                "doc": '{("a\d":"b")x?-2}',
                "obj": {"a1": "b", "a2": "b", "a3": "b"},
                "want": "At location $ - failed to match the following JSON pairs: [\"a1\": \"b\", \"a2\": \"b\", \"a3\": \"b\"]",
            },
            {
                "name": "Object ellipsis (1)",
                "doc": '{..., "c": "d"}',
                "obj": {"c": "e"},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [\"c\": \"d\", ...]",
            },
            {
                "name": "Object ellipsis (2)",
                "doc": '{(string:*)x?, "c": "d"}',
                "obj": {"c": "e"},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [\"c\": \"d\", (string: *)x?]",
            },
            {
                "name": "Object capture with paris and ellipsis (1)",
                "doc": '{("a\d":"b")x?,"c":"d", ... }',
                "obj": {"c": "d1"},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [\"c\": \"d\", (\"a\d\": \"b\")x?, ...]",
            },
        ]
        self._bad_match(test_cases)