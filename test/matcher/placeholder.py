"""JSPEC Testing Module for matching JSPEC documents for a placeholder.
"""

from test.matcher import JSPECTestMatcher

class JSPECTestMatcherPlaceholder(JSPECTestMatcher):
    """Class for testing the behaviour when using the ``match`` method for
    placeholders.

    A valid JSPEC placeholder one of array, boolean, int, null, object, real or
    string.
    """

    def test_matcher_placeholder_good(self):
        """Test examples of good matches.
        The ``match`` method should return a matching ``JSPEC`` with a
        placeholder as its element.
        """
        test_cases = [
            {
                "name": "Object placeholder",
                "doc": "object",
                "obj": {},
            },
            {
                "name": "Array placeholder",
                "doc": "array",
                "obj": [],
            },
            {
                "name": "String placeholder",
                "doc": "string",
                "obj": "",
            },
            {
                "name": "Integer placeholder",
                "doc": "int",
                "obj": 0,
            },
            {
                "name": "Real placeholder",
                "doc": "real",
                "obj": 0.0,
            },
            {
                "name": "Number placeholder (1)",
                "doc": "number",
                "obj": 0,
            },
            {
                "name": "Number placeholder (2)",
                "doc": "number",
                "obj": 0.0,
            },
            {
                "name": "Bool placeholder",
                "doc": "bool",
                "obj": False,
            },
            {
                "name": "Object placeholder, not empty",
                "doc": "object",
                "obj": {"key": "val", "a": 5, "s": {"b":[]}},
            },
            {
                "name": "Array placeholder, not empty",
                "doc": "array",
                "obj": [1, 2, 3, 4, 5],
            },
            {
                "name": "String placeholder, not empty",
                "doc": "string",
                "obj": "something",
            },
            {
                "name": "Integer placeholder, not zero",
                "doc": "int",
                "obj": 1348239,
            },
            {
                "name": "Real placeholder, not zero",
                "doc": "real",
                "obj": -27.34310,
            },
            {
                "name": "Number placeholder, not zero",
                "doc": "number",
                "obj": 1348239,
            },
            {
                "name": "Number placeholder, not zero",
                "doc": "number",
                "obj": -27.34310,
            },
            {
                "name": "Bool placeholder, not False",
                "doc": "bool",
                "obj": True,
            },
            {
                "name": "Int more than or equal to (1)",
                "doc": "int >= 10",
                "obj": 30,
            },
            {
                "name": "Int more than or equal to (2)",
                "doc": "int >= 10",
                "obj": 10,
            },
            {
                "name": "Int more than",
                "doc": "int > 10",
                "obj": 30,
            },
            {
                "name": "Int less than or equal to (1)",
                "doc": "int <= 10",
                "obj": 2,
            },
            {
                "name": "Int less than or equal to (2)",
                "doc": "int <= 10",
                "obj": 10,
            },
            {
                "name": "Int less than",
                "doc": "int < 10",
                "obj": 2,
            },
            {
                "name": "Real more than or equal to (1)",
                "doc": "real >= 10.5",
                "obj": 30.7,
            },
            {
                "name": "Real more than or equal to (2)",
                "doc": "real >= 10.0",
                "obj": 10.0,
            },
            {
                "name": "Real more than",
                "doc": "real > 10.5",
                "obj": 30.7,
            },
            {
                "name": "Real less than or equal to (1)",
                "doc": "real <= 10.0",
                "obj": 2.6,
            },
            {
                "name": "Real less than or equal to (2)",
                "doc": "real <= 10.5",
                "obj": 10.5,
            },
            {
                "name": "Real less than",
                "doc": "real < 10.5",
                "obj": 2.9,
            },
            {
                "name": "Number more than or equal to (1)",
                "doc": "number >= 10.3",
                "obj": 30,
            },
            {
                "name": "Number more than or equal to (2)",
                "doc": "number >= 10",
                "obj": 10.3,
            },
            {
                "name": "Number more than",
                "doc": "number > 10",
                "obj": 10.2,
            },
            {
                "name": "Number less than or equal to (1)",
                "doc": "number <= 10.12",
                "obj": 2,
            },
            {
                "name": "Number less than or equal to (2)",
                "doc": "number <= 10.7",
                "obj": 10,
            },
            {
                "name": "Number less than",
                "doc": "number < 10",
                "obj": 2.5,
            },
        ]
        self._good_match(test_cases)

    def test_matcher_placeholder_bad(self):
        """Test examples of bad matches.
        The ``match`` method should not return a matching ``JSPEC`` with the
        specified placeholder as its element.
        """
        test_cases = [
            {
                "name": "Unwanted array",
                "doc": "object",
                "obj": [],
                "want": "At location $ - expected an object",
            },
            {
                "name": "Unwanted object",
                "doc": "array",
                "obj": {},
                "want": "At location $ - expected an array",
            },
            {
                "name": "Unwanted string",
                "doc": "string",
                "obj": [],
                "want": "At location $ - expected a string",
            },
            {
                "name": "Unexpected null",
                "doc": "bool",
                "obj": None,
                "want": "At location $ - expected a boolean",
            },
            {
                "name": "Unwanted real",
                "doc": "int",
                "obj": 0.0,
                "want": "At location $ - expected an int",
            },
            {
                "name": "Unexpected int",
                "doc": "real",
                "obj": 0,
                "want": "At location $ - expected a real",
            },
            {
                "name": "Unexpected string",
                "doc": "number",
                "obj": "notanumber",
                "want": "At location $ - expected a number",
            },
            {
                "name": "Not Int more than or equal to",
                "doc": "int >= 10",
                "obj": 2,
                "want": "At location $ - expected an int that is more than or equal to '10', got '2'",
            },
            {
                "name": "Not Int more than (1)",
                "doc": "int > 10",
                "obj": 10,
                "want": "At location $ - expected an int that is more than '10', got '10'",
            },
            {
                "name": "Not Int more than (2)",
                "doc": "int > 10",
                "obj": 9,
                "want": "At location $ - expected an int that is more than '10', got '9'",
            },
            {
                "name": "Not Int less than or equal to",
                "doc": "int <= 10",
                "obj": 20,
                "want": "At location $ - expected an int that is less than or equal to '10', got '20'",
            },
            {
                "name": "Not Int less than (1)",
                "doc": "int < 10",
                "obj": 10,
                "want": "At location $ - expected an int that is less than '10', got '10'",
            },
            {
                "name": "Not Int less than (2)",
                "doc": "int < 10",
                "obj": 11,
                "want": "At location $ - expected an int that is less than '10', got '11'",
            },
            {
                "name": "Not Real more than or equal to",
                "doc": "real >= 10.5",
                "obj": 9.5,
                "want": "At location $ - expected a real that is more than or equal to '10.5', got '9.5'",
            },
            {
                "name": "Not Real more than (1)",
                "doc": "real > 10.5",
                "obj": 10.5,
                "want": "At location $ - expected a real that is more than '10.5', got '10.5'",
            },
            {
                "name": "Not Real more than (2)",
                "doc": "real > 10.5",
                "obj": 7.5,
                "want": "At location $ - expected a real that is more than '10.5', got '7.5'",
            },
            {
                "name": "Not Real less than or equal to",
                "doc": "real <= 10.5",
                "obj": 19.5,
                "want": "At location $ - expected a real that is less than or equal to '10.5', got '19.5'",
            },
            {
                "name": "Not Real less than (1)",
                "doc": "real < 10.0",
                "obj": 10.0,
                "want": "At location $ - expected a real that is less than '10.0', got '10.0'",
            },
            {
                "name": "Not Real less than (2)",
                "doc": "real < 10.0",
                "obj": 10.1,
                "want": "At location $ - expected a real that is less than '10.0', got '10.1'",
            },
            {
                "name": "Not Number more than or equal to",
                "doc": "number >= 10.3",
                "obj": 3,
                "want": "At location $ - expected a number that is more than or equal to '10.3', got '3'",
            },
            {
                "name": "Not Number more than (1)",
                "doc": "number > 10.2",
                "obj": 10.2,
                "want": "At location $ - expected a number that is more than '10.2', got '10.2'",
            },
            {
                "name": "Not Number more than (2)",
                "doc": "number > 10.2",
                "obj": 10,
                "want": "At location $ - expected a number that is more than '10.2', got '10'",
            },
            {
                "name": "Not Number less than or equal to",
                "doc": "number <= 10.3",
                "obj": 30,
                "want": "At location $ - expected a number that is less than or equal to '10.3', got '30'",
            },
            {
                "name": "Not Number less than (1)",
                "doc": "number < 10",
                "obj": 10,
                "want": "At location $ - expected a number that is less than '10', got '10'",
            },
            {
                "name": "Not Number less than (2)",
                "doc": "number < 10",
                "obj": 10.8,
                "want": "At location $ - expected a number that is less than '10', got '10.8'",
            },
        ]
        self._bad_match(test_cases)