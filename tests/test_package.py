from importlib import resources


def test_package_declares_inline_typing_support():
    assert resources.files("jsonpath_ng").joinpath("py.typed").is_file()
