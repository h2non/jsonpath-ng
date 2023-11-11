"""
Tests for the jsonpath.py command line interface.
"""

import io
import json
import os
import sys

from jsonpath_ng.bin.jsonpath import main


def test_stdin_mode(monkeypatch, capsys):
    stdin_text = json.dumps(
        {
            "foo": {
                "baz": 1,
                "bizzle": {"baz": 2},
            },
        }
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))

    main("jsonpath.py", "foo..baz")

    stdout, _ = capsys.readouterr()
    assert stdout == "1\n2\n"


def test_filename_mode(capsys):
    test1 = os.path.join(os.path.dirname(__file__), "test1.json")
    test2 = os.path.join(os.path.dirname(__file__), "test2.json")

    main("jsonpath.py", "foo..baz", test1, test2)

    stdout, _ = capsys.readouterr()
    assert stdout == "1\n2\n3\n4\n"
