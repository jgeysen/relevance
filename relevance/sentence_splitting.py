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
    Sentences are deemed to be part of a table if they meet the following criteria:
    1. The sentence contains less than 5 actual words AND the sentence contains more than 5 consecutive full stops or spaces
    2. The sentence has more words containing digits than actual words AND the number of words containing digits is not zero.

    If a sentence meet criteria 1 or 2, the sentence is removed from the dataframe.

    Args:
            df_spacy (DataFrame): pandas dataframe containing the articles.
            The column containing the sentences has as header 'sentences'. No other column is required.

    Returns:
            df_returns (DataFrame): pandas dataframe returning the sentences where words containing digits have been dropped.
    """
    # split the sentences on spaces, store as list for each sentence
    df_spacy["split_on_spaces"] = df_spacy.sentences.str.split()
    # length of the list of the sentence splitted on spaces => number of words/numbers/symbols in the sentence.
    df_spacy["total_length"] = df_spacy.split_on_spaces.str.len()
    # number of strings which don't contain any numbers (= deemed 'actual words') for each sentence
    df_spacy["nr_of_actual_words"] = [
        len([i for i in x if hasNumbers(i) is False]) for x in df_spacy.split_on_spaces
    ]
    # number of strings which contain one or more numbers for each sentence
    df_spacy["nr_of_digits"] = (
        df_spacy.total_length.values - df_spacy.nr_of_actual_words.values
    )
    # Boolean column, true if the sentence contains more than 5 consecutive spaces or full stops.
    df_spacy["contains_spacing_fullstops"] = df_spacy.sentences.str.contains(
        r".*\s{5,}.*|.*\.{5,}.*", regex=True
    )
    # Boolean column, true if the sentence contains more strings containing no digits than strings containing digits.
    df_spacy["more_words_than_digits"] = (
        df_spacy.nr_of_actual_words.values > df_spacy.nr_of_digits.values
    )

    z = {
        "var1": eval("df_spacy.nr_of_actual_words <= 5"),
        "var2": eval("df_spacy.contains_spacing_fullstops == True"),
        "var3": eval("df_spacy.more_words_than_digits == False"),
        "var4": eval("df_spacy.nr_of_digits != 0"),
    }
    # following sentences are deemed to be (a part of) a table:
    # 1. The sentence contains less than 5 actual words AND the sentence contains more than 5 consecutive full stops or spaces
    # 2. The sentence has more words containing digits than actual words AND the number of words containing digits is not zero.
    index_tables = df_spacy[
        ((z["var1"]) & (z["var2"])) | ((z["var3"]) & (z["var4"]))
    ].index
    # only select those sentences which aren't selected by the above rules.
    df_spacy = df_spacy[~df_spacy.index.isin(index_tables)]

    # drop the columns used for identifying the (sentences which are part of the) tables.
    df_returns = df_spacy.reset_index(drop=True).drop(
        [
            "nr_of_actual_words",
            "nr_of_digits",
            "contains_spacing_fullstops",
            "more_words_than_digits",
            "total_length",
            "split_on_spaces",
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
    # Add a numerical column containing the length of the sentence, when split on spaces.
    df_nltk["length"] = [len(sentence.split(" ")) for sentence in df_nltk.sentences]
    # add a position column to the dataframe, which describes the sentence position in the article:
    df_nltk["position"] = 1
    df_nltk["position"] = df_nltk.groupby(["identifier"], sort=False)[
        "position"
    ].transform(pd.Series.cumsum)
    # Add an art_length column, which is the length of the article measured in number of sentences.
    # First make a dataframe art_lengths contains for each identifier the number of times it occurs in the df_nltk.
    art_lengths = pd.DataFrame(
        df_nltk.groupby(["identifier"], sort=False).size(), columns=["art_length"]
    ).reset_index(drop=False)
    # Merge the art_lengths dataframe with the df_nltk on the identifier.
    df_nltk = pd.merge(df_nltk, art_lengths, on="identifier")

    if combination == "previous":
        # When we want to merge short sentences with the previous sentence in an article, we want to avoid merging the first (short) sentence
        # of an article with the last sentence of the previous article. For this reason, we initialise the lenght of the first sentence always
        # with the minimum length of a long sentence.
        df_nltk.loc[df_nltk.position == 1, "length"] = min_length
        df_nltk_long = df_nltk[df_nltk.length >= min_length]
        df_nltk_short = df_nltk[df_nltk.length < min_length]
        if len(df_nltk_short) > 0:
            # Map the indices of all short sentences onto the nearest lower index of the long sentences.
            df_nltk_short.index = [
                min(df_nltk_long.index, key=lambda x: (abs(x - y), x))
                for y in df_nltk_short.index.tolist()
            ]
            # Concat long and short sentence dataframes, don't reset the indices!
            result = pd.concat(
                [df_nltk_long, df_nltk_short], ignore_index=False, sort=False
            ).reset_index()
            # join all sentences with the same index in the final dataframe. This joins short and long sentences into one sentence.
            df_returns = pd.DataFrame(
                result.groupby(["index"])["sentences"].apply(lambda x: " ".join(x)),
                columns=["sentences"],
            )
            df_returns["identifier"] = (
                result.groupby(["index"])["identifier"].min().tolist()
            )

    # if combination == "next":
    # 	# When we want to merge short sentences with the previous sentence in an article, we want to avoid merging the first (short) sentence
    # 	# of an article with the last sentence of the previous article. For this reason, we initialise the lenght of the first sentence always
    # 	# with the minimum length of a long sentence.
    #     df_nltk.loc[df_nltk.position == 1, "length"] = min_length
    #     df_nltk_long = df_nltk[df_nltk.length >= min_length]
    #     df_nltk_short = df_nltk[df_nltk.length < min_length]
    #     if len(df_nltk_short) > 0:
    #     	# Map the indices of all short sentences onto the nearest lower index of the long sentences.
    #         df_nltk_short.index = [min(df_nltk_long.index, key=lambda x: (abs(x - y), x)) for y in df_nltk_short.index.tolist()]
    #         # Concat long and short sentence dataframes, don't reset the indices!
    #         result = pd.concat([df_nltk_long, df_nltk_short], ignore_index=False, sort=False).reset_index()
    #         # join all sentences with the same index in the final dataframe. This joins short and long sentences into one sentence.
    #         df_returns = pd.DataFrame(result.groupby(['index'])['sentences'].apply(lambda x: ' '.join(x)),columns=['sentences'])
    #         df_returns['identifier'] = result.groupby(['index'])['identifier'].min().tolist()

    df_returns = df_returns.reset_index(drop=True)

    return df_returns
