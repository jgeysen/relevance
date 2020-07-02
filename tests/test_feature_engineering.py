import numpy as np
import pandas as pd

from relevance.feature_engineering import (
    add_features,
    create_features,
    preprocess_regex,
)


def test_preprocess_regex() -> None:
    entity_list = ["Aviva"]
    regex_dict = {"Aviva": {"alias": ["Aviva"], "abbrev": ["Aviva"]}}
    all_regex_list = [
        "aviva",
        "[^a-zA-Z]+aviva[^a-zA-Z]+",
        "^aviva[^a-zA-Z]+",
        "[^a-zA-Z]+aviva$",
        "^aviva$",
    ]
    all_regex_dict = {
        "alias": ["aviva"],
        "abbrev": [
            "[^a-zA-Z]+aviva[^a-zA-Z]+",
            "^aviva[^a-zA-Z]+",
            "[^a-zA-Z]+aviva$",
            "^aviva$",
        ],
    }
    assert (preprocess_regex(entity_list, regex_dict)) == (
        all_regex_list,
        all_regex_dict,
    )


def test_add_features() -> None:
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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

    regex_list = [
        "aviva",
        "[^a-zA-Z]+aviva[^a-zA-Z]+",
        "^aviva[^a-zA-Z]+",
        "[^a-zA-Z]+aviva$",
        "^aviva$",
    ]

    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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
                [1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 1],
                [4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 1],
            )
        ),
        columns=["sentences", "identifier", "position", "total_length"],
    )
    assert np.array_equal(
        add_features(input1_df, regex_list)[0].position.values,
        output1_df.position.values,
    )


def test_create_features() -> None:
    target = False
    entity_list = ["Aviva"]
    regex_dict = {"Aviva": {"alias": ["Aviva"], "abbrev": ["Aviva"]}}
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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
                [1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 1],
                [4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 1],
            )
        ),
        columns=["sentences", "identifier", "position", "total_length"],
    )
    # all_regex_dict = {
    #     "alias": ["aviva"],
    #     "abbrev": [
    #         "[^a-zA-Z]+aviva[^a-zA-Z]+",
    #         "^aviva[^a-zA-Z]+",
    #         "[^a-zA-Z]+aviva$",
    #         "^aviva$",
    #     ],
    # }
    assert np.array_equal(
        create_features(input1_df, regex_dict, entity_list, target)[0].position.values,
        output1_df.position.values,
    )

    target = True
    entity_list = ["Aviva"]
    regex_dict = {"Aviva": {"alias": ["Aviva"], "abbrev": ["Aviva"]}}
    input1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            )
        ),
        columns=["sentences", "identifier", "Aviva"],
    )
    output1_df = pd.DataFrame(
        list(
            zip(
                [
                    "This is the first sentence of the first article, which mentions Aviva.",
                    "Short sentence, no entity mentioned.",
                    "This is a much longer intermediate sentence of the article, Aviva.",
                    "Final one.",
                    "This is the first sentence of a second article, Aviva is mentioned here.",
                    "Short sentence1.",
                    "Short sentence2, let's mention Aviva.",
                    "Another short one which has a verb.",
                    "A long sentence, short sentences should be parsed to this one.",
                    "Final sentence of the second article: Aviva.",
                    "First sentence of a third article, which only has one sentence: Aviva.",
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
                [1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 1],
                [4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            )
        ),
        columns=["sentences", "identifier", "position", "total_length", "target"],
    )
    # all_regex_dict = {
    #     "alias": ["aviva"],
    #     "abbrev": [
    #         "[^a-zA-Z]+aviva[^a-zA-Z]+",
    #         "^aviva[^a-zA-Z]+",
    #         "[^a-zA-Z]+aviva$",
    #         "^aviva$",
    #     ],
    # }
    assert np.array_equal(
        create_features(input1_df, regex_dict, entity_list, target)[0].position.values,
        output1_df.position.values,
    )
