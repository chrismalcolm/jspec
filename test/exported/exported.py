import unittest
import os
import jspec

from jspec.entity import (
    JSPEC, 
    JSPECObject,
    JSPECObjectPair,
    JSPECString,
)

class JSPECTestExported(unittest.TestCase):
    """Class for testing the functions in the ``jspec.__init__`` module.
    """

    LONG_DOCUMENT = """
    {//Comment 1
        "A field for object": {
            "hello": "world"
        },
        "B field for array": [
            [],
            {},
            5
        ],
        "C field for string": "\w\d",
        "D field for int": 3,
        "E field for real": 10.01,
        "F field for boolean": true,
        "G field for null": null,
        "H field for wildcard": *,
        "I field for negation": !4,
        "J field for macro": <ENV_1>,
        "K field for conditional": (1 | 3 ^ 4 & 2),
        "L field for placeholders": [
            object,
            array,
            string, //Comment 2
            bool,
            int,
            real,
            number
        ],
        "M field for array capture": [
            1,
            "a",
            (1 | 7),
            (2 | 3)x?,
            (6 | 5)x4,
            (5 | 7)x2-?,
            (8 | 0)x?-3,
            (2 | 4)x?-?,
            (1 | 8)x6-7
        ],
        "N field for array ellipsis": [
            3,
            4,
            ...
        ],
        "O field for object capture": {
            "red": "brick",
            "blue": "sky",
            ("a": 1 | "b": 8),
            ("b": 2 | "b": 8)x?,
            ("c": 3 | "b": 8)x4,
            ("d": 4 | "b": 8)x2-?,
            ("e": 5 | "b": 8)x?-3,
            ("f": 6 | "b": 8)x?-?,
            ("g": 7 | "b": 8)x6-7
        }, //Comment 4
        "P field for object ellipsis": {
            "red": "brick",
            "blue": "sky",
            ...
        },
        "Q field for different variations of reals": [
            1e-10,
            1.00001,
            1.9E7,
            1.0E4,
            1000.0
        ],/*
        Comment 5
        */
        "R field for inequalities": [
            int < 5,
            int > 6,
            int <= 5,
            int >= 6,
            real < 5.2,
            real > 6.2,
            real <= 5.2,
            real >= 6.2,
            number < 5,
            number > 6,
            number <= 5,
            number >= 6
        ]
    }   
    """

    PRETTY_DOCUMENT = """{ //Comment 1
    "A field for object": {
        "hello": "world"
    },
    "B field for array": [
        [],
        {},
        5
    ],
    "C field for string": "\w\d",
    "D field for int": 3,
    "E field for real": 10.01,
    "F field for boolean": true,
    "G field for null": null,
    "H field for wildcard": *,
    "I field for negation": !4,
    "J field for macro": <ENV_1>,
    "K field for conditional": (1 | 3 ^ 4 & 2),
    "L field for placeholders": [
        object,
        array,
        string, //Comment 2
        bool,
        int,
        real,
        number
    ],
    "M field for array capture": [
        1,
        "a",
        (1 | 7)x1,
        (2 | 3)x?,
        (6 | 5)x4,
        (5 | 7)x2-?,
        (8 | 0)x?-3,
        (2 | 4)x?,
        (1 | 8)x6-7
    ],
    "N field for array ellipsis": [
        3,
        4,
        ...
    ],
    "O field for object capture": {
        "blue": "sky",
        "red": "brick",
        ("a": 1 | "b": 8)x1,
        ("b": 2 | "b": 8)x?,
        ("c": 3 | "b": 8)x4,
        ("d": 4 | "b": 8)x2-?,
        ("e": 5 | "b": 8)x?-3,
        ("f": 6 | "b": 8)x?,
        ("g": 7 | "b": 8)x6-7
    }, //Comment 4
    "P field for object ellipsis": {
        "blue": "sky",
        "red": "brick",
        ...
    },
    "Q field for different variations of reals": [
        1e-10,
        1.00001,
        1.9E7,
        1.0E4,
        1000.0
    ], /*
        Comment 5
        */ 
    "R field for inequalities": [
        int < 5,
        int > 6,
        int <= 5,
        int >= 6,
        real < 5.2,
        real > 6.2,
        real <= 5.2,
        real >= 6.2,
        number < 5,
        number > 6,
        number <= 5,
        number >= 6
    ]
}"""

    def test_load(self):
        """Test the ``jspec.load`` function."""
        with open("./test/assets/load.jspec", "r") as f:
            spec = jspec.load(f)
        self.assertEqual(
            spec,
            JSPEC(
                JSPECObject({
                    JSPECObjectPair(
                        (JSPECString("key"), JSPECString("value"))
                    ),
                }),
            ),
        )

    def test_load_pretty(self):
        """Test the ``jspec.load`` function."""
        with open("./test/assets/load.jspec", "r") as f:
            spec = jspec.load(f, pretty=True)
        self.assertEqual(
            spec,
            JSPEC(
                JSPECObject({
                    JSPECObjectPair(
                        (JSPECString("key"), JSPECString("value"))
                    ),
                }),
            ),
        )
        self.assertEqual(
            str(spec),
            '{\n\t"key": "value"\n}',
        )

    def test_loads(self):
        """Test the ``jspec.loads`` function."""
        spec = jspec.loads('{"key": "value"}')
        self.assertEqual(
            spec,
            JSPEC(
                JSPECObject({
                    JSPECObjectPair(
                        (JSPECString("key"), JSPECString("value"))
                    ),
                }),
            ),
        )
        exc = None
        try:
            jspec.loads(1)
        except TypeError as err:
            exc = err
        self.assertEqual(
            str(exc),
            "Expecting a string not <class 'int'>",
        )

    def test_loads_pretty(self):
        """Test the ``jspec.loads`` function."""
        spec = jspec.loads('{"key": "value"}', pretty=True)
        self.assertEqual(
            spec,
            JSPEC(
                JSPECObject({
                    JSPECObjectPair(
                        (JSPECString("key"), JSPECString("value"))
                    ),
                }),
            ),
        )
        err = None
        try:
            spec = jspec.loads('{"key": value}', pretty=True)
        except jspec.scanner.JSPECDecodeError as jde:
            err = jde
        self.assertNotEqual(
            err,
            None
        )
        err = None
        try:
            spec = jspec.loads('{"key": "value"}', pretty=True, indent=" xa\t")
        except TypeError as vle:
            err = vle
        self.assertNotEqual(
            err,
            None
        )
        spec = jspec.loads(self.LONG_DOCUMENT, pretty=True, indent='    ')
        self.assertEqual(
            str(spec),
            self.PRETTY_DOCUMENT,
        )        

    def test_dump(self):
        """Test the ``jspec.dump`` function."""
        spec = JSPEC(
            JSPECObject({
                JSPECObjectPair(
                    (JSPECString("key"), JSPECString("value"))
                ),
            }),
        )
        with open("./test/assets/dump.jspec", "w") as f:
            jspec.dump(spec, f)

        with open("./test/assets/dump.jspec", "r") as f:
            text = f.read()

        with open("./test/assets/dump.jspec", "w") as f:
            f.truncate(0)
        
        self.assertEqual(text, '{"key": "value"}')

    def test_dumps(self):
        """Test the ``jspec.dumps`` function."""
        spec = JSPEC(
            JSPECObject({
                JSPECObjectPair(
                    (JSPECString("key"), JSPECString("value"))
                ),
            }),
        )
        document = jspec.dumps(spec)
        self.assertEqual(document, '{"key": "value"}')
        exc = None
        try:
            jspec.dumps(1)
        except TypeError as err:
            exc = err
        self.assertEqual(
            str(exc),
            "Expecting a JSPEC not <class 'int'>",
        )

    def test_check(self):
        """Test the ``jspec.check`` function."""
        spec = JSPEC(
            JSPECObject({
                JSPECObjectPair(
                    (JSPECString("key"), JSPECString("value"))
                ),
            }),
        )
        element = {"key": "value"}
        self.assertTrue(jspec.check(spec, element))
        os.environ["MY_ID"] = '1'
        with open("./test/assets/test.jspec", "r") as f:
            spec = jspec.load(f)
        element = {
            "id": 1,
            "timestamp": 1530.5,
            "data": [
                {
                    "longitude": 10.2,
                    "latitude": 41.3,
                },
                {
                    "longitude": 33.3,
                    "latitude": 76.2,
                },
                {
                    "longitude": 9.5,
                    "latitude": 12.1,
                }
            ],
            "other": "data"
        }
        res, _ = jspec.check(spec, element)
        self.assertTrue(res)

    def test_checks(self):
        """Test the ``jspec.checks`` function."""
        document = '{"key": "value"}'
        element = {"key": "value"}
        self.assertTrue(jspec.checks(document, element))
        exc = None
        try:
            jspec.check(1, 0)
        except TypeError as err:
            exc = err
        self.assertEqual(
            str(exc),
            "Expecting a JSPEC not <class 'int'>",
        )

    def test_serialization(self):
        spec = jspec.loads(self.LONG_DOCUMENT)
        want = '{"A field for object": {"hello": "world"}, "B field for array": [[], {}, 5], "C field for string": "\w\d", "D field for int": 3, "E field for real": 10.01, "F field for boolean": true, "G field for null": null, "H field for wildcard": *, "I field for negation": !4, "J field for macro": <ENV_1>, "K field for conditional": (1 | 3 ^ 4 & 2), "L field for placeholders": [object, array, string, bool, int, real, number], "M field for array capture": [1, "a", (1 | 7)x1, (2 | 3)x?, (6 | 5)x4, (5 | 7)x2-?, (8 | 0)x?-3, (2 | 4)x?, (1 | 8)x6-7], "N field for array ellipsis": [3, 4, ...], "O field for object capture": {"blue": "sky", "red": "brick", ("a": 1 | "b": 8)x1, ("b": 2 | "b": 8)x?, ("c": 3 | "b": 8)x4, ("d": 4 | "b": 8)x2-?, ("e": 5 | "b": 8)x?-3, ("f": 6 | "b": 8)x?, ("g": 7 | "b": 8)x6-7}, "P field for object ellipsis": {"blue": "sky", "red": "brick", ...}, "Q field for different variations of reals": [1e-10, 1.00001, 1.9E7, 1.0E4, 1000.0], "R field for inequalities": [int < 5, int > 6, int <= 5, int >= 6, real < 5.2, real > 6.2, real <= 5.2, real >= 6.2, number < 5, number > 6, number <= 5, number >= 6]}'
        got = jspec.dumps(spec)
        self.assertEqual(want, got)