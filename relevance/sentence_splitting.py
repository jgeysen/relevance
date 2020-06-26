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

    This function excludes tables from an reuters article. Tables are not sentences, so they can/have to be removed.

    Args:
            df_spacy (DataFrame): pandas dataframe containing the articles. The column containing the sentences has as header 'sentences'.

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
