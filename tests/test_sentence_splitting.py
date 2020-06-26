import pandas as pd

from relevance.sentence_splitting import (
    exclude_tables,
    hasNumbers,
    parse_short_sentences,
)


def test_hasNumbers() -> None:
    assert hasNumbers("5test") is True
    assert hasNumbers("test") is False


def test_exclude_tables() -> None:
    input_df = pd.DataFrame(["test", "           4"], columns=["sentences"])
    output_df = pd.DataFrame(["test"], columns=["sentences"])
    assert exclude_tables(input_df).sentences.values == output_df.sentences.values


def test_parse_short_sentences() -> None:
    input_df = pd.DataFrame(
        list(zip(["test test test test test test test test"], ["test"])),
        columns=["sentences", "identifier"],
    )
    output_df = pd.DataFrame(
        list(zip(["test test test test test test test test"], ["test"])),
        columns=["sentences", "identifier"],
    )
    min_length = 3
    combination = "previous"
    assert (
        parse_short_sentences(input_df, min_length, combination).sentences.values
        == output_df.sentences.values
    )
