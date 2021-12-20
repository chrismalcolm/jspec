"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherObject``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherObject(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    objects.

    A JSPEC object will match a object with matching key-element pairs.
    """

    def test_matcher_object_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECObject`` as its element.
        """
        test_cases = [
            {
                "name": "Empty object",
                "doc": "{}",
                "obj": {},
            },
            {
                "name": "Sample",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2, "c": 3},
            },
            {
                "name": "Embedded",
                "doc": '{"a": {"b": {"c": 3}}}',
                "obj": {"a": {"b": {"c": 3}}},
            },
        ]
        self._good_match(test_cases)

    def test_matcher_object_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECObject`` as its element.
        """
        test_cases = [
            {
                "name": "Empty object not array",
                "doc": "{}",
                "obj": [],
                "want": "At location $ - expected an object",
            },
            {
                "name": "Incorrect values by unmatched key",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2, "x": 3, "y":4},
                "want": 'At location $ - failed to match the following JSON pairs: ["x": 3, "y": 4]'
            },
            {
                "name": "Incorrect values by unmatched key (1)",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2, "c": 4},
                "want": "At location $.c - expected '3', got '4'",
            },
            {
                "name": "Incorrect values by unmatched key (2)",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2, "c": 3, "y":4},
                "want": 'At location $ - exhausted JSPEC object, failed to match the following JSON pairs: ["y": 4]',
            },
            {
                "name": "Incorrect values by unmatched key (3)",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2, "c": 3, "y":4, "z": 5},
                "want": 'At location $ - exhausted JSPEC object, failed to match the following JSON pairs: ["y": 4, "z": 5]',
            },
            {
                "name": "Wrong order embedded",
                "doc": '{"a": {"b": {"c": 3}}}',
                "obj": {"a": {"c": {"b": 3}}},
                "want": "At location $.a - regex pattern 'b' failed to match '\"c\"'",
            },
            {
                "name": "Incorrect values by unmatched key (1)",
                "doc": '{"a": 1, "b": 2}',
                "obj": {"a": 1, "b": 2, "c": 3},
                "want": "At location $ - exhausted JSPEC object, failed to match the following JSON pairs: [\"c\": 3]",
            },
            {
                "name": "Incorrect values by unmatched key (2)",
                "doc": '{"a": 1, "b": 2, "c": 3}',
                "obj": {"a": 1, "b": 2},
                "want": "At location $ - exhausted JSON object, failed to match the following JSPEC pairs: [\"c\": 3]",
            },
        ]
        self._bad_match(test_cases)