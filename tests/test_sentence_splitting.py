import numpy as np
import pandas as pd
import spacy

from relevance.sentence_splitting import (
    exclude_tables,
    hasNumbers,
    nltk_processing,
    parse_short_sentences,
    select_actual_sentences,
    sentence_splitting,
    spacy_processing,
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
                    "Short sentence1.",
                    "Short sentence2.",
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
                    "article_id2",
                    "article_id3",
                ],
            )
        ),
        columns=["sentences", "identifier"],
    )

    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "First sentence of the first article. Short sentence.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one. Final one.",
                    "First sentence of a second article. Short sentence1. Short sentence2.",
                    "A long sentence, short sentences should be parsed to this one. Another short one.",
                    "Final sentence of the second article.",
                    "First sentence of a third article, which only has one sentence.",
                ],
                [
                    "article_id1",
                    "article_id1",
                    "article_id2",
                    "article_id2",
                    "article_id2",
                    "article_id3",
                ],
            )
        ),
        columns=["sentences", "identifier"],
    )
    min_length = 4
    combination = "previous"
    assert np.array_equal(
        parse_short_sentences(input1_df, min_length, combination).sentences.values,
        output1_df.sentences.values,
    )


def test_select_actual_sentences() -> None:
    spacy_pipe = spacy.load(
        "en_core_web_sm",
        disable=[
            "tagger",
            "ner",
            "entity_linker",
            "merge_noun_chunks",
            "merge_entities",
            "merge_subtokens",
        ],
    )
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article.",
                    "Short sentence.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one.",
                    "Final one.",
                    "This is the first sentence of a second article.",
                    "Short sentence1.",
                    "Short sentence2.",
                    "Another short one which has a verb.",
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
                    "article_id2",
                    "article_id3",
                ],
            )
        ),
        columns=["sentences", "identifier"],
    )

    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one.",
                    "This is the first sentence of a second article.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "First sentence of a third article, which only has one sentence.",
                ],
                [
                    "article_id1",
                    "article_id1",
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
        select_actual_sentences(input1_df, spacy_pipe).sentences.values,
        output1_df.sentences.values,
    )


def test_spacy_processing() -> None:
    spacy_pipe = spacy.load(
        "en_core_web_sm",
        disable=[
            "tagger",
            "ner",
            "entity_linker",
            "merge_noun_chunks",
            "merge_entities",
            "merge_subtokens",
        ],
    )
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article. This is another sentence of the article. 1...... 1        1 1 2 Table. This is a sentence again 3, with some numbers 1 1. 34      ."
                ],
                ["article_id1"],
            )
        ),
        columns=["article_body", "identifier"],
    )
    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article. This is another sentence of the article. This is a sentence again 3, with some numbers 1 1."
                ],
                ["article_id1"],
            )
        ),
        columns=["article_body", "identifier"],
    )

    assert np.array_equal(
        spacy_processing(input1_df, spacy_pipe).article_body.values,
        output1_df.article_body.values,
    )


def test_nltk_processing() -> None:
    # nltk.data.load("tokenizers/punkt/english.pickle")
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article. This is a short sentence. Another short sentence. Third short one. This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one. Final sentence."
                ],
                ["article_id1"],
            )
        ),
        columns=["article_body", "identifier"],
    )
    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article. This is a short sentence. Another short sentence.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one. Third short one. Final sentence.",
                ],
                ["article_id1", "article_id1"],
            )
        ),
        columns=["sentences", "identifier"],
    )

    assert np.array_equal(
        nltk_processing(input1_df).sentences.values, output1_df.sentences.values
    )


def test_sentence_splitting() -> None:
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article. This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one."
                ],
                ["article_id1"],
            )
        ),
        columns=["article_body", "identifier"],
    )
    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article.",
                    "This is a much longer intermediate sentence of the article, rather short sentences before and after should be parsed to this one.",
                ],
                ["article_id1", "article_id1"],
            )
        ),
        columns=["sentences", "identifier"],
    )
    assert np.array_equal(
        sentence_splitting(input1_df).sentences.values, output1_df.sentences.values
    )
