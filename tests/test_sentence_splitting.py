import numpy as np
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
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "First sentence of the first article.",
                    "Short sentence.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one.",
                    "Final one.",
                    "First sentence of a second article.",
                    "Short sentence.",
                    "Another short one.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article.",
                    "First sentence of a third article, which only has one sentence.",
                ],
                [
                    "article_id1",
                    "article_id1",
                    "article_id1",
                    "article_id1",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id3",
                ],
            )
        ),
        columns=["sentences", "identifier"],
    )

    # output1_df = pd.DataFrame(
    #     list(
    #         zip(
    #             [
    #                 "First sentence of the first article.",
    #                 "Short sentence. This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one.",
    #                 "Final one.",
    #                 "First sentence of a second article.",
    #                 "Short sentence. Another short one.",
    #                 "A long sentence, short sentences should be parsed to this one.",
    #                 "Final sentence of the second article.",
    #                 "First sentence of a third article, which only has one sentence.",
    #             ],
    #             [
    #                 "article_id1",
    #                 "article_id1",
    #                 "article_id1",
    #                 "article_id2",
    #                 "article_id2",
    #                 "article_id2",
    #                 "article_id2",
    #                 "article_id3",
    #             ],
    #         )
    #     ),
    #     columns=["sentences", "identifier"],
    # )
    # min_length = 3
    # combination = "next"
    # assert np.array_equal(
    #     parse_short_sentences(input1_df, min_length, combination).sentences.values,
    #     output1_df.sentences.values,
    # )
    min_length = 3
    combination = "previous"
    output2_df = pd.DataFrame(
        list(
            zip(
                [
                    "First sentence of the first article. Short sentence.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one. ",
                    "Final one. ",
                    "First sentence of a second article. Short sentence.",
                    "Another short one. ",
                    "A long sentence, short sentences should be parsed to this one. ",
                    "Final sentence of the second article. ",
                    "First sentence of a third article, which only has one sentence. ",
                ],
                [
                    "article_id1",
                    "article_id1",
                    "article_id1",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id3",
                ],
            )
        ),
        columns=["sentences", "identifier"],
    )

    assert np.array_equal(
        parse_short_sentences(input1_df, min_length, combination).sentences.values,
        output2_df.sentences.values,
    )
