import unittest
import subprocess

class JSPECTestCheck(unittest.TestCase):
    """Class for testing the functions in the ``jspec.check`` module.
    """

    def test_command_line_scripts_usage_1_1(self):
        """Test the command line tool for check - Usage (1.1)."""
        result = subprocess.run(['python3', '-m', 'jspec.check', './test/assets/load.jspec', './test/assets/load.json'], stdout=subprocess.PIPE)
        self.assertEqual(
            result.stdout,
            b''
        )

    def test_command_line_scripts_usage_1_2(self):
        """Test the command line tool for check - Usage (1.2)."""
        result = subprocess.run(['python3', '-m', 'jspec.check', './test/assets/load.jspec', '--raw-json={"key": 2}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(
            result.stdout,
            b'At location $.key - expected a string, got \'2\'\n'
        )

    def test_command_line_scripts_usage_1_3(self):
        """Test the command line tool for check - Usage (1.3)."""
        result = subprocess.run(['python3', '-m', 'jspec.check', '--raw-json=[1,2,3,4]', '--raw-jspec=[1,...,4]'], stdout=subprocess.PIPE)
        self.assertEqual(
            result.stdout,
            b''
        )
        