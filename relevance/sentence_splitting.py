"""
Article cleaning and relevance filtering project
=========================================================
The core module of the project
"""
# import packages
import pandas as pd

# ***************************************************************************************
# *********************************FUNCTIONS*********************************************
# **************************************************************************************

# following function checks if the given inputstring contains a digit:


def hasNumbers(inputString: str) -> bool:
    """Check if a string contains numbers function.

    Function which returns true if there's a digit in the inputstring.

    Args:
            inputString (str): a string

    Returns:
            Boolean (bool): True if the inputString contains a digit.
    """
    return any(char.isdigit() for char in inputString)


def exclude_tables(df_spacy: pd.DataFrame) -> pd.DataFrame:
    """Exclude tables function.

    This function excludes tables from an reuters article. Tables are not sentences, so they have to be removed.

    Args:
            df_spacy (DataFrame): pandas dataframe containing the articles.
            The column containing the sentences has as header 'sentences'. No other column is required.

    Returns:
            df_returns (DataFrame): pandas dataframe returning the sentences where words containing digits have been dropped.
    """
    df_spacy["split"] = df_spacy.sentences.str.split()
    df_spacy["total_length"] = df_spacy.split.str.len()

    df_spacy["nr_of_actual_words"] = [
        len([i for i in x if hasNumbers(i) is False]) for x in df_spacy.split
    ]
    df_spacy["nr_of_digits"] = (
        df_spacy.total_length.values - df_spacy.nr_of_actual_words.values
    )
    df_spacy["contains_spacing_fullstops"] = df_spacy.sentences.str.contains(
        r"\s{8}|\.{8}", regex=True
    )
    df_spacy["more_words_than_digits"] = (
        df_spacy.nr_of_actual_words.values > df_spacy.nr_of_digits.values
    )

    z = {
        "var1": eval("df_spacy.nr_of_actual_words <= 5"),
        "var2": eval("df_spacy.contains_spacing_fullstops == True"),
        "var3": eval("df_spacy.more_words_than_digits == False"),
        "var4": eval("df_spacy.nr_of_digits != 0"),
    }

    index_tables = df_spacy[
        ((z["var1"]) & (z["var2"])) | ((z["var3"]) & (z["var4"]))
    ].index
    df_spacy = df_spacy[~df_spacy.index.isin(index_tables)].drop(["split"], axis=1)

    df_returns = df_spacy.reset_index(drop=True).drop(
        [
            "nr_of_actual_words",
            "nr_of_digits",
            "contains_spacing_fullstops",
            "more_words_than_digits",
            "total_length",
        ],
        axis=1,
    )

    return df_returns


def parse_short_sentences(
    df_nltk: pd.DataFrame, min_length: int, combination: str
) -> pd.DataFrame:
    """Parse short sentences to long sentences.

    This function parses short sentences to longer ones.

    Args:
        df_nltk (DataFrame): pandas dataframe containing sentences. This dataframe should have the following
        columns: sentences, identifier (article level).
        min_length (int): The minimum length of the sentences to be parsed into longer ones.
        combination (str): Can have three values; 'previous' indicating short sentences are parsed with
        the previous sentence, 'next' indicating short sentences are parsed with the next sentence.

    Returns:
        df_returns (DataFrame): pandas dataframe containing the sentences after parsing.
    """
    df_nltk["length"] = [len(sentence.split(" ")) for sentence in df_nltk.sentences]
    # add a position column to the dataframe, which describes the sentence position in the article:
    df_nltk["position"] = 1
    df_nltk["position"] = df_nltk.groupby(["identifier"], sort=False)[
        "position"
    ].transform(pd.Series.cumsum)
    # Length of the article (absolute, number of sentences)
    art_lengths = pd.DataFrame(
        df_nltk.groupby(["identifier"], sort=False).size(), columns=["art_length"]
    ).reset_index(drop=False)
    df_nltk = pd.merge(df_nltk, art_lengths, on="identifier")
    # reset the lengths of the first and last sentence of an article to the threshold,
    # to make sure these aren't shifted.
    df_nltk.loc[df_nltk.position == 1, "length"] = min_length
    df_nltk.loc[df_nltk.position == df_nltk.art_length, "length"] = min_length
    # df_nltk = df_nltk.drop(["position", "art_length"], axis=1)

    df_nltk_long = df_nltk[df_nltk.length >= min_length]
    df_nltk_short = df_nltk[df_nltk.length < min_length]
    if len(df_nltk_short) > 0:
        if combination == "previous":
            df_nltk_short.index = [x - 1 for x in df_nltk_short.index.tolist()]
            df_nltk_long = df_nltk_long.merge(
                df_nltk_short, left_index=True, right_index=True, how="left"
            ).fillna("")

        if combination == "next":
            df_nltk_short.index = [x + 1 for x in df_nltk_short.index.tolist()]
            df_nltk_long = df_nltk_short.merge(
                df_nltk_long, left_index=True, right_index=True, how="right"
            ).fillna("")

        df_nltk_long["sentences"] = (
            df_nltk_long.sentences_x.array + " " + df_nltk_long.sentences_y.array
        )

        df_nltk_long["identifier"] = [
            x + y if x == "" else x
            for x, y in zip(df_nltk_long.identifier_x, df_nltk_long.identifier_y)
        ]
        df_nltk_long = df_nltk_long[["sentences", "identifier"]]

    df_returns = df_nltk_long.reset_index(drop=True)

    return df_returns
