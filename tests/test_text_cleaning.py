from relevance.text_cleaning import add_spacing, remove_reuters_lingo


def test_remove_reuters_lingo() -> None:
    assert remove_reuters_lingo("test") == "test"


def test_add_spacing() -> None:
    assert add_spacing("test") == "test"
