"""Test module for the JSPEC examples."""

import unittest
import jspec


class JspecTest(unittest.TestCase):
    """Class for testing JSPEC examples."""

    def test_load_from_file(self):
        """"Test loading JSPEC from a file"""
        with open("./fixtures/example.jspec") as f:
            spec = jspec.load(f)

        with open("./fixtures/example.json") as f:
            result = spec.match(f)

        self.assertTrue(result.result())