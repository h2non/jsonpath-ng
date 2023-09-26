# Standard library imports
import unittest
import logging
import io
import sys
import os
import json

from jsonpath_ng.bin.jsonpath import main

class TestJsonPathScript(unittest.TestCase):
    """
    Tests for the jsonpath.py command line interface.
    """

    @classmethod
    def setup_class(cls):
        logging.basicConfig()

    def setUp(self):
        self.input = io.StringIO()
        self.output = io.StringIO()
        self.saved_stdout = sys.stdout
        self.saved_stdin = sys.stdin
        sys.stdout = self.output
        sys.stdin = self.input

    def tearDown(self):
        self.output.close()
        self.input.close()
        sys.stdout = self.saved_stdout
        sys.stdin = self.saved_stdin

    def test_stdin_mode(self):
        # 'format' is a benign Python 2/3 way of ensuring it is a text type rather than binary
        self.input.write('{0}'.format(json.dumps({
            'foo': {
                'baz': 1,
                'bizzle': {
                    'baz': 2
                }
            }
        })))
        self.input.seek(0)
        main('jsonpath.py', 'foo..baz')
        self.assertEqual(self.output.getvalue(), '1\n2\n')

    def test_filename_mode(self):
        test1 = os.path.join(os.path.dirname(__file__), 'test1.json')
        test2 = os.path.join(os.path.dirname(__file__), 'test2.json')
        main('jsonpath.py', 'foo..baz', test1, test2)
        self.assertEqual(self.output.getvalue(), '1\n2\n3\n4\n')

