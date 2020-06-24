from relevance.text_cleaning import remove_reuters_lingo


def test_remove_reuters_lingo() -> None:
    assert remove_reuters_lingo("test") == "test"
