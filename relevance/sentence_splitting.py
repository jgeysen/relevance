"""
Article cleaning and relevance filtering project
=========================================================
The core module of the project
"""
import nltk
import numpy as np
import pandas as pd
import spacy

# def sentence_splitting_for_dataframes(df: pd.DataFrame) -> pd.DataFrame:
# 	"""Overarching function which splits reuters articles into sentences, optimized for a dataframe.

# 	This function does the following:
# 	1. Load spacy and nltk pipes
# 	2. Call the spacy_processing function on the dataframe to use spacy to split the article into sentences and exclude tables.
# 	3. Call the nltk_processing fucntion on the dataframe to use nltk to split the article into sentences, short sentences are parsed to the nearest longest sentence.
# 	4. Only selecting those nltk sentences which contain at least one subject, object and verb.

# 	It returns a dataframe with sentences.

# 	Args:
# 		df: (DataFrame):

# 	Returns:
# 		df_sents (DataFrame):

# 	"""
#     spacy_pipe = spacy.load('en_core_web_sm',disable=['tagger',
#                                                       'ner',
#                                                       'entity_linker',
#                                                       'merge_noun_chunks',
#                                                       'merge_entities',
#                                                       'merge_subtokens'])
#     nltk_pipe = nltk.data.load('tokenizers/punkt/english.pickle')
#     # throw out: 'Reuters euro Eurobond new issue index'
#     #df = df[df.title != 'Reuters euro Eurobond new issue index'].reset_index(drop=True)

#     # df at this point is a dataframe of articles.
#     df_new = spacy_processing(df,spacy_pipe)
#     df_sents = nltk_processing(df_new,nltk_pipe)

#     # final check: Each sentence contains a subject, object and verb, using spacy again:
#     df_sents = select_actual_sentences(df_sents,spacy_pipe)
#     #return sents
#     return df_sents

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
            # Map the indices of all short sentences onto the nearest index of the long sentences.
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


# this function checks if each of the given sentences actually contain a subject, object and verb.
def select_actual_sentences(
    df: pd.DataFrame, spacy_pipe: spacy.pipeline
) -> pd.DataFrame:
    """Select actual sentences, which contain a verb, subject and object.

    This function uses the spacy dependency labels and selects those sentences which contain a verb, object and subject.

    Args:
        df (DataFrame): A dataframe containing a column 'sentences'.
        spacy_pipe (spacy_pipe): Spacy pipe object, given on a function level, because loading it outside the function is more efficient.

    Returns:
        df (DataFrame): A dataframe which only contains sentences with at least one verb, subject and object.
    """
    # define what verbs, objects and subjects are. This information is found in the Spacy documentation.
    verbs = ["ROOT", "acl"]
    subjects = ["subj", "nsubj", "csubj", "nsubjpass", "compound"]
    objects = ["obj", "dobj", "pobj"]

    # Create a spacy object for each sentence. Store this object in a new column 'spacy_object' in the dataframe
    df["spacy_object"] = [spacy_pipe(sentence) for sentence in df.sentences]
    # Call the dependency label for each token in the object. Store in new column 'dep_labels' in dataframe.
    df["dep_labels"] = [[token.dep_ for token in x] for x in df.spacy_object]

    # create three new columns, each containing the number of verbs, subjects and objects in each sentence.
    # Calculate this number by calculating the length of the list containing the cross section between the dep_labels and the above defined lists.
    df["verbs"] = [len([lbl for lbl in x if lbl in verbs]) for x in df.dep_labels]
    df["subjects"] = [len([lbl for lbl in x if lbl in subjects]) for x in df.dep_labels]
    df["objects"] = [len([lbl for lbl in x if lbl in objects]) for x in df.dep_labels]

    # To be regarded a valid sentence, there needs to be at least one verb, one subject and one object.
    z = {
        "var1": eval("df.verbs > 0"),
        "var2": eval("df.subjects > 0"),
        "var3": eval("df.objects > 0"),
    }

    # Slice the dataframe according to the conditions.
    df = (
        df[(z["var1"]) & (z["var2"]) & (z["var3"])]
        .drop(["verbs", "subjects", "objects", "dep_labels", "spacy_object"], axis=1)
        .reset_index(drop=True)
    )

    return df


def spacy_processing(df: pd.DataFrame, spacy_pipe: spacy.pipeline) -> pd.DataFrame:
    """Processing the articles using spacy functionality.

    This function does the following:
    1. The spacy sentisizer splits the articles in sentences.
    2. Using the 'exclude_tables' functionality in the sentence_splitting module, tables can be differentiated from sentences.
    3. After excluding the tables from the article, the sentences are parsed back together into a processed article body and returned.

    Args:
        df (DataFrame): Dataframe containing a column 'article_body' containing article bodies.
        spacy_pipe (spacy_pipe): spacy pipe object, called/loaded/passed on a function level for efficiency.

    Returns:
        df_new (DataFrame): Dataframe containing article body after excluding tables.
    """
    # SPACY:
    df["spacy_object"] = [spacy_pipe(x) for x in df.article_body.array]
    df["sentences"] = [
        [sent.string.strip() for sent in doc.sents] for doc in df.spacy_object.array
    ]
    lens = [len(item) for item in df["sentences"]]
    df_spacy = pd.DataFrame(
        {
            "identifier": np.repeat(df["identifier"].values, lens),
            # "title" : np.repeat(df['title'].values,lens),
            "sentences": np.concatenate(df["sentences"].values),
        }
    )

    # exclude table sentences:
    df_spacy = exclude_tables(df_spacy)
    # Parse back together:ze
    df_new = (
        df_spacy.groupby("identifier")["sentences"]
        .apply(list)
        .reset_index(name="sentences_1")
    )
    # parse the sentences back together using join:
    df_new["article_body"] = [" ".join(sentence) for sentence in df_new.sentences_1]
    # parse the sentences back together using join:
    # df_new["article_body"] = [
    #    re.sub(r"\n|\r", " ", article) for article in df_new.article_body
    # ]

    df_new = df_new.drop(["sentences_1"], axis=1)

    return df_new


def nltk_processing(df: pd.DataFrame):
    """Processing the articles using NLTK.

    This function does the following:
    1. Use the NLTK senticiser to split the article into sentences.
    2. Parse short sentences together with the parse_short_sentences functionality in the sentence_splitting module.

    Args:
        df (pd.DataFrame): kk

    Returns:
        df_nltk (pd.DataFrame): kk
    """
    nltk_pipe = nltk.data.load("tokenizers/punkt/english.pickle")
    # create a nltk_object for each article body in the article_body column:
    df["nltk_object"] = [nltk_pipe.tokenize(doc) for doc in df.article_body]
    # Extract the sentences from the nltk object, save as a list in the 'sentences' column:
    df["sentences"] = [
        [sentence for (n, sentence) in enumerate(doc)] for doc in df.nltk_object
    ]
    # list containing the lengths of the sentences:
    lens = [len(item) for item in df["sentences"]]
    # unfold the sentences in the list in the sentence column to an equal number of rows in df_nltk dataframe:
    df_nltk = pd.DataFrame(
        {
            "identifier": np.repeat(df["identifier"].values, lens),
            # "title" : np.repeat(df['title'].values,lens),
            "sentences": np.concatenate(df["sentences"].values),
        }
    )
    # NLTK senticizer is very accurate. If there would be extremely short sentences left, merge them with the nearest long sentence:
    df_nltk = parse_short_sentences(df_nltk, min_length=10, combination="previous")
    return df_nltk
