from relevance.text_cleaning import (
    add_spacing,
    clean_reuters_article,
    remove_reuters_lingo,
    remove_spacing,
)


def test_remove_reuters_lingo() -> None:
    assert remove_reuters_lingo("test") == "test"


def test_add_spacing() -> None:
    assert add_spacing("test") == "test"


def test_remove_spacing() -> None:
    assert remove_spacing("test") == "test"


def test_clean_reuters_article() -> None:
    assert clean_reuters_article("test") == "test"
