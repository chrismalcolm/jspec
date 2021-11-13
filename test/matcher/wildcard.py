"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherWildcard``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherWildcard(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    wildcards.

    A JSPEC wildcard will match any element.
    """

    def test_matcher_wildcard_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECWildcard`` as its element.
        """
        test_cases = [
            {
                "name": "Object wildcard",
                "doc": "*",
                "obj": {},
            },
            {
                "name": "Array wildcard",
                "doc": "*",
                "obj": [],
            },
            {
                "name": "String wildcard",
                "doc": "*",
                "obj": "",
            },
            {
                "name": "Integer wildcard",
                "doc": "*",
                "obj": 0,
            },
            {
                "name": "Real wildcard",
                "doc": "*",
                "obj": 0.0,
            },
            {
                "name": "Bool wildcard",
                "doc": "*",
                "obj": False,
            },
            {
                "name": "Object wildcard, not empty",
                "doc": "*",
                "obj": {"key": "val", "a": 5, "s": {"b":[]}},
            },
            {
                "name": "Array wildcard, not empty",
                "doc": "*",
                "obj": [1, 3, 5, 6],
            },
            {
                "name": "String wildcard, not empty",
                "doc": "*",
                "obj": "xyzabc",
            },
            {
                "name": "Integer wildcard, not zero",
                "doc": "*",
                "obj": 1348239,
            },
            {
                "name": "Real wildcard, not zero",
                "doc": "*",
                "obj": -27.34310,
            },
            {
                "name": "Bool wildcard, not False",
                "doc": "*",
                "obj": True,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_wildcard_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECWildcard`` as its element.
        """
        class Other:

            def __init__(self):
                pass

        other = Other()
        test_cases = [
            {
                "name": "Non-JSON object",
                "doc": "*",
                "obj": other,
                "want": "At location $ - expected a Python native JSON element, not %s" % other.__class__,
            },
        ]
        self._bad_match(test_cases)