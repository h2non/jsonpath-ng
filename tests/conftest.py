import pytest


@pytest.fixture(autouse=True)
def disable_auto_id_field(monkeypatch):
    monkeypatch.setattr("jsonpath_ng.jsonpath.auto_id_field", None)


@pytest.fixture()
def auto_id_field(monkeypatch, disable_auto_id_field):
    """Enable `jsonpath_ng.jsonpath.auto_id_field`."""

    field_name = "id"
    monkeypatch.setattr("jsonpath_ng.jsonpath.auto_id_field", field_name)
    return field_name
