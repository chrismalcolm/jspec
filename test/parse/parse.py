import unittest
import subprocess

class JSPECTestParse(unittest.TestCase):
    """Class for testing the functions in the ``jspec.parse`` module.
    """

    def test_command_line_scripts_usage_1_1(self):
        """Test the command line tool for parser - Usage (1.1)."""
        result = subprocess.run(['python3', '-m', 'jspec.parse', './test/assets/load.jspec'], stdout=subprocess.PIPE)
        self.assertEqual(
            result.stdout,
            b'{\n    "key": "value"\n}\n'
        )

    def test_command_line_scripts_usage_1_2(self):
        """Test the command line tool for parser - Usage (1.2)."""
        result = subprocess.run(['python3', '-m', 'jspec.parse', './test/assets/load.jspec', '--indent=\t'], stdout=subprocess.PIPE)
        self.assertEqual(
            result.stdout,
            b'{\n\t"key": "value"\n}\n'
        )

    def test_command_line_scripts_usage_1_3(self):
        """Test the command line tool for parser - Usage (1.3)."""
        outfile = './test/assets/parse.jspec'
        subprocess.run(['python3', '-m', 'jspec.parse', './test/assets/load.jspec', outfile], stdout=subprocess.PIPE)
        with open(outfile, 'r+') as f:
            text = f.read()
            f.truncate(0)
        self.assertEqual(
            text,
            '{\n    "key": "value"\n}\n'
        )

    def test_command_line_scripts_usage_2_1(self):
        """Test the command line tool for parser - Usage (2.1)."""
        stdin = '{"jspec": "term", ...}'
        p = subprocess.Popen(['python3', '-m', 'jspec.parse'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate(input=stdin.encode())[0]
        self.assertEqual(
            output,
            b'{\n    "jspec": "term",\n    ...\n}\n'
        )

    def test_command_line_scripts_usage_2_2(self):
        """Test the command line tool for parser - Usage (2.2)."""
        stdin = '{"jspec": "term", ...}'
        p = subprocess.Popen(['python3', '-m', 'jspec.parse', '--pretty=false'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate(input=stdin.encode())[0]
        self.assertEqual(
            output,
            b'{"jspec": "term", ...}\n'
        )

    def test_command_line_scripts_usage_2_3(self):
        """Test the command line tool for parser - Usage (2.3)."""
        stdin = '[1,2,,4]'
        p = subprocess.Popen(['python3', '-m', 'jspec.parse'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate(input=stdin.encode())[0]
        self.assertEqual(
            output,
            b'Expecting JSPEC term in array: line 1 column 6 (char 5)\n'
        )


