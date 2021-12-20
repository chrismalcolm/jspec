"""JSPEC Testing Module for matchning JSPEC documents for
``JSPECTestMatcherArrayCaptureElement``.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherArrayCapture(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    array captures.

    A JSPEC array capture will match a consecutive set of elements, which all
    match at least one of the elements in the array capture.
    """

    def test_matcher_array_capture_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with
        ``JSPECArrayCaptureGroup``.
        """
        test_cases = [
            {
                "name": "Basic array capture no multiplier",
                "doc": '[(1)]',
                "obj": [1],
            },
            {
                "name": "Basic array capture (1.0)",
                "doc": '[(1)x?]',
                "obj": [1,1,1,1],
            },
            {
                "name": "Basic array capture (1.1)",
                "doc": '[(1)x?]',
                "obj": [1],
            },
            {
                "name": "Basic array capture (1.2)",
                "doc": '[(1)x?]',
                "obj": [],
            },
            {
                "name": "Basic array capture (2)",
                "doc": '[(1)x2]',
                "obj": [1,1],
            },
            {
                "name": "Basic array capture (3.1)",
                "doc": '[(1)x2-?]',
                "obj": [1,1],
            },
            {
                "name": "Basic array capture (3.2)",
                "doc": '[(1)x2-?]',
                "obj": [1,1,1,1,1,1],
            },
            {
                "name": "Basic array capture (4.1)",
                "doc": '[(1)x?-4]',
                "obj": [1,1,1,1],
            },
            {
                "name": "Basic array capture (4.2)",
                "doc": '[(1)x?-4]',
                "obj": [1,1],
            },
            {
                "name": "Basic array capture (4.3)",
                "doc": '[(1)x?-4]',
                "obj": [],
            },
            {
                "name": "Basic array capture (5.1)",
                "doc": '[(1)x3-5]',
                "obj": [1,1,1],
            },
            {
                "name": "Basic array capture (5.2)",
                "doc": '[(1)x3-5]',
                "obj": [1,1,1,1],
            },
            {
                "name": "Basic array capture (5.3)",
                "doc": '[(1)x3-5]',
                "obj": [1,1,1,1,1],
            },
            {
                "name": "Basic array capture with condition",
                "doc": '[(1 ^ 3)x?]',
                "obj": [1,3,1,3,1],
            },
            {
                "name": "Array capture with elements",
                "doc": '[5,(1)x?,4]',
                "obj": [5,1,1,1,4],
            },
            {
                "name": "Array capture with elements and condition",
                "doc": '[5,(!1 & !2)x?,4]',
                "obj": [5,"a","b",4],
            },
            {
                "name": "Basic array capture with multiplier",
                "doc": '[(1)x5]',
                "obj": [1,1,1,1,1],
            },
            {
                "name": "Array capture with elements with multiplier",
                "doc": '[5,(1)x1,4]',
                "obj": [5,1,4],
            },
            {
                "name": "Array capture with elements with multiplier and condition",
                "doc": '[5,(1 | 2)x5,4]',
                "obj": [5,1,1,2,2,1,4],
            },
            {
                "name": "Multiple Array capture (1)",
                "doc": '[(1 | 2)x?,3, (5 | 4)x?]',
                "obj": [3],
            },
            {
                "name": "Multiple Array capture (2)",
                "doc": '[(1 | 2)x?,3, (5 | 4)x?]',
                "obj": [1,1,3],
            },
            {
                "name": "Multiple Array capture (3)",
                "doc": '[(1 | 2)x?,3, (5 | 4)x?]',
                "obj": [1,1,3,5,4],
            },
            {
                "name": "Multiple Array capture (4)",
                "doc": '[(1 | 2)x?,3, (5 | 4)x?]',
                "obj": [3,5,4],
            },
            {
                "name": "All capture (1)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [],
            },
            {
                "name": "All capture (2)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [1,1,2,2],
            },
            {
                "name": "All capture (3)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [3,3],
            },
            {
                "name": "All capture (4)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [1,1,3],
            },
            {
                "name": "All capture (5)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [1,1,2,2,3,3],
            },
            {
                "name": "Array ellipsis (1)",
                "doc": '[...]',
                "obj": [1,1,2,2,3,3],
            },
            {
                "name": "Array ellipsis (2)",
                "doc": '[...]',
                "obj": [],
            },
            {
                "name": "Array ellipsis (3)",
                "doc": '[(*)x?]',
                "obj": [],
            },
            {
                "name": "Array ellipsis (4)",
                "doc": '[(*)x?]',
                "obj": [5,5,5,5,1],
            },
            {
                "name": "Array ellipsis with elements (1)",
                "doc": '[2 ,... ,6]',
                "obj": [2, 6],
            },
            {
                "name": "Array ellipsis with elements (2)",
                "doc": '[2 ,... ,6]',
                "obj": [2,3,4,5,6],
            },
            
        ]
        self._good_match(test_cases)

    def test_matcher_array_capture_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with
        ``JSPECArrayCaptureGroup``.
        """
        test_cases = [
            {
                "name": "Basic array capture no multiplier",
                "doc": '[(1)]',
                "obj": [2],
                "want": "At location $ - failed array capture, '2' failed to match '(1)x1'",
            },
            {
                "name": "Basic array capture no multiplier",
                "doc": '[(1)]',
                "obj": [],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x1'",
            },
            {
                "name": "Basic array capture (1.0)",
                "doc": '[(1)x?]',
                "obj": [2],
                "want": "At location $[0] - exhausted JSPEC array, no JSPEC term left to match '2'",
            },
            {
                "name": "Basic array capture (2.0)",
                "doc": '[(1)x2]',
                "obj": [1],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x2'",
            },
            {
                "name": "Basic array capture (2.1)",
                "doc": '[(1)x2]',
                "obj": [],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x2'",
            },
            {
                "name": "Basic array capture (2.2)",
                "doc": '[(1)x2]',
                "obj": [1,1,1],
                "want": "At location $[2] - exhausted JSPEC array, no JSPEC term left to match '1'",
            },
            {
                "name": "Basic array capture (3.0)",
                "doc": '[(1)x4-5]',
                "obj": [1,1,1],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x4-5'",
            },
            {
                "name": "Basic array capture (3.1)",
                "doc": '[(1)x4-5]',
                "obj": [],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x4-5'",
            },
            {
                "name": "Basic array capture (3.2)",
                "doc": '[(1)x4-5]',
                "obj": [1,1,1,1,1,1],
                "want": "At location $[5] - exhausted JSPEC array, no JSPEC term left to match '1'",
            },
            {
                "name": "Basic array capture (4.0)",
                "doc": '[(1)x4-?]',
                "obj": [1,1,1],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x4-?'",
            },
            {
                "name": "Basic array capture (4.1)",
                "doc": '[(1)x4-?]',
                "obj": [],
                "want": "At location $ - exhausted JSON array, no JSON element left to match '(1)x4-?'",
            },
            {
                "name": "Basic array capture (5.0)",
                "doc": '[(1)x?-5]',
                "obj": [1,1,1,1,1,1],
                "want": "At location $[5] - exhausted JSPEC array, no JSPEC term left to match '1'",
            },
            {
                "name": "All capture (1)",
                "doc": '[(1)x?,(2)x?,(3)x?]',
                "obj": [3,2],
                "want": "At location $[1] - exhausted JSPEC array, no JSPEC term left to match '2'",
            },
        ]
        self._bad_match(test_cases)