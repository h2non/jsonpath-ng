"""Tests for find_values() convenience method."""
import json
from jsonpath_ng.ext import parse

STORE = {
    "store": {
        "book": [
            {"category": "reference", "author": "Nigel Rees", "title": "Sayings", "price": 8.95},
            {"category": "fiction", "author": "Evelyn Waugh", "title": "Sword", "price": 12.99},
            {"category": "fiction", "author": "Herman Melville", "title": "Moby", "isbn": "0-553-21311-3", "price": 8.99},
            {"category": "fiction", "author": "J. R. R. Tolkien", "title": "LOTR", "isbn": "0-395-19395-8", "price": 22.99},
        ],
        "bicycle": {"color": "red", "price": 19.95},
    }
}


def test_find_values_simple():
    path = parse("$.store.bicycle.color")
    assert path.find_values(STORE) == ["red"]


def test_find_values_matches_find():
    for expr in [
        "$.store.book[*].title",
        "$..author",
        "$..book[?(@.isbn)]",
        "$.store.book[?(@.price < 10)].title",
        "$.store.book[?(@.price >= 12.99)].title",
        "$..book[0,1].title",
        "$.store.book[:2].title",
    ]:
        path = parse(expr)
        expected = [m.value for m in path.find(STORE)]
        assert path.find_values(STORE) == expected, f"mismatch for {expr}"


def test_find_values_filter_str():
    path = parse("$.store.book[?(@.category == 'fiction')].title")
    result = path.find_values(STORE)
    assert result == ["Sword", "Moby", "LOTR"]


def test_find_values_filter_and():
    path = parse("$.store.book[?(@.price < 10 & @.category == 'fiction')].title")
    result = path.find_values(STORE)
    assert result == ["Moby"]


def test_find_values_descendant():
    path = parse("$..price")
    result = path.find_values(STORE)
    assert len(result) == 5


def test_find_values_empty():
    path = parse("$.nonexistent")
    assert path.find_values(STORE) == []
