"""JSPEC Testing Module for matching JSPEC documents for
``JSPECTestMatcherString``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherString(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    strings.

    A JSPEC string will match a string which matches the regex of the JSPEC
    string.
    """

    def test_matcher_string_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        ``JSPECString`` as its element.
        """
        test_cases = [
            {
                "name": "Simple string",
                "doc": '"basic"',
                "obj": "basic",
            },
            {
                "name": "Matches gray or grey",
                "doc": '"gray|grey"',
                "obj": "grey",
            },
            {
                "name": "Escape character",
                "doc": '"gray\|grey"',
                "obj": "gray|grey",
            },
            {
                "name": "Matches z's",
                "doc": '"z{3,6}"',
                "obj": "zzzzz",
            },
            {
                "name": "Matches regex, regexes, regexp or regexps",
                "doc": '"rege(x(es)?|xps?)"',
                "obj": "regexps",
            },
            {
                "name": "Matches an empty string",
                "doc": '""',
                "obj": "",
            },
        ]
        self._good_match(test_cases)

    def test_matcher_string_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECString`` as its element.
        """
        test_cases = [
            {
                "name": "Bad match",
                "doc": '"basic"',
                "obj": "complex",
                "want": "At location $ - regex pattern 'basic' failed to match '\"complex\"'",
            },
            {
                "name": "Bad regex match",
                "doc": '"gray|grey"',
                "obj": "grxy",
                "want": "At location $ - regex pattern 'gray|grey' failed to match '\"grxy\"'",
            },
            {
                "name": "No empty string",
                "doc": '""',
                "obj": "not empty",
                "want": "At location $ - regex pattern '' failed to match '\"not empty\"'",
            },
            {
                "name": "Escape character",
                "doc": '"gray\|grey"',
                "obj": "gray",
                "want": "At location $ - regex pattern 'gray\|grey' failed to match '\"gray\"'",
            },
        ]
        self._bad_match(test_cases)