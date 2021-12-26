import unittest
import jspec

from jspec.entity import (
    JSPEC, 
    JSPECObject,
    JSPECObjectPair,
    JSPECString,
)

class JSPECTestExported(unittest.TestCase):
    """Class for testing the function in the ``jspec.__init__`` module.
    """
    def test_load(self):
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

    def test_loads(self):
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

    def test_loads_bad(self):
        exc = None
        try:
            jspec.loads(1)
        except TypeError as err:
            exc = err
        self.assertEqual(
            str(exc),
            "Expecting a string not <class 'int'>",
        )

    def test_dump(self):
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
        spec = JSPEC(
            JSPECObject({
                JSPECObjectPair(
                    (JSPECString("key"), JSPECString("value"))
                ),
            }),
        )
        document = jspec.dumps(spec)
        self.assertEqual(document, '{"key": "value"}')

    def test_dumps_bad(self):
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
        spec = JSPEC(
            JSPECObject({
                JSPECObjectPair(
                    (JSPECString("key"), JSPECString("value"))
                ),
            }),
        )
        element = {"key": "value"}
        self.assertTrue(jspec.check(spec, element))

    def test_checks(self):
        document = '{"key": "value"}'
        element = {"key": "value"}
        self.assertTrue(jspec.checks(document, element))

    def test_check_bad(self):
        exc = None
        try:
            jspec.check(1, 0)
        except TypeError as err:
            exc = err
        self.assertEqual(
            str(exc),
            "Expecting a JSPEC not <class 'int'>",
        )