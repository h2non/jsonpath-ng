import argparse as argparse
import glob as glob
import json as json
import sys as sys
from collections.abc import Iterable
from typing import IO

from ..jsonpath import DatumInContext, JSONPath
from ..parser import parse as parse

def find_matches_for_file(expr: JSONPath, f: IO[str]) -> list[DatumInContext[object]]: ...
def print_matches(matches: Iterable[DatumInContext[object]]) -> None: ...
def main(*argv: str) -> None: ...
def entry_point() -> None: ...
