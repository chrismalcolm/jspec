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
                "obj": {"a": 1, "b": 2, "x": 3},
                "want": 'At location $ - the following object keys were unmatched: "x"',
            },
            {
                "name": "Wrong order embedded",
                "doc": '{"a": {"b": {"c": 3}}}',
                "obj": {"a": {"c": {"b": 3}}},
                "want": 'At location $ - the following object keys were unmatched: "x"',
            },
        ]
        # TODO uncomment and add tests once code works for matching objects
        #self._bad_match(test_cases)