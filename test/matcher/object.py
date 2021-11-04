"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherObject``.
"""

from test.matcher import JSPECTestMatcher
from jspec.component import (
    JSPEC, 
    JSPECObject,
)

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
        test_cases = []
        self._good_match(test_cases)

    def test_matcher_object_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified ``JSPECObject`` as its element.
        """
        test_cases = []
        self._bad_match(test_cases)