import pandas as pd

from relevance.sentence_splitting import exclude_tables, hasNumbers


def test_hasNumbers() -> None:
    assert hasNumbers("5test") is True
    assert hasNumbers("test") is False


def test_exclude_tables() -> None:
    input_df = pd.DataFrame(["test", "           4"], columns=["sentences"])
    output_df = pd.DataFrame(["test"], columns=["sentences"])
    assert exclude_tables(input_df).sentences.values == output_df.sentences.values
