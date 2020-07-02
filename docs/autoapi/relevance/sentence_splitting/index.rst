:mod:`relevance.sentence_splitting`
===================================

.. py:module:: relevance.sentence_splitting

.. autoapi-nested-parse::

   Article cleaning and relevance filtering project
   =========================================================
   The core module of the project



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   relevance.sentence_splitting.hasNumbers
   relevance.sentence_splitting.exclude_tables
   relevance.sentence_splitting.parse_short_sentences
   relevance.sentence_splitting.select_actual_sentences


.. function:: hasNumbers(inputString: str) -> bool

   Check if a string contains numbers function.

   Function which returns true if there's a digit in the inputstring.

   :param inputString: a string
   :type inputString: str

   :returns: *Boolean (bool)* -- True if the inputString contains a digit.


.. function:: exclude_tables(df_spacy: pd.DataFrame) -> pd.DataFrame

   Exclude tables function.

   This function excludes tables from an reuters article. Tables are not sentences, so they have to be removed.
   Sentences are deemed to be part of a table if they meet the following criteria:
   1. The sentence contains less than 5 actual words AND the sentence contains more than 5 consecutive full stops or spaces
   2. The sentence has more words containing digits than actual words AND the number of words containing digits is not zero.

   If a sentence meet criteria 1 or 2, the sentence is removed from the dataframe.

   :param df_spacy: pandas dataframe containing the articles.
   :type df_spacy: DataFrame
   :param The column containing the sentences has as header 'sentences'. No other column is required.:

   :returns: *df_returns (DataFrame)* -- pandas dataframe returning the sentences where words containing digits have been dropped.


.. function:: parse_short_sentences(df_nltk: pd.DataFrame, min_length: int, combination: str) -> pd.DataFrame

   Parse short sentences to long sentences.

   This function parses short sentences to longer ones.

   :param df_nltk: pandas dataframe containing sentences. This dataframe should have the following
   :type df_nltk: DataFrame
   :param columns: sentences, identifier (article level).
   :param min_length: The minimum length of the sentences to be parsed into longer ones.
   :type min_length: int
   :param combination: Can have three values; 'previous' indicating short sentences are parsed with
   :type combination: str
   :param the previous sentence, 'next' indicating short sentences are parsed with the next sentence.:

   :returns: *df_returns (DataFrame)* -- pandas dataframe containing the sentences after parsing.


.. function:: select_actual_sentences(df: pd.DataFrame, spacy_pipe: spacy.pipeline) -> pd.DataFrame

   Select actual sentences, which contain a verb, subject and object.

   This function uses the spacy dependency labels and selects those sentences which contain a verb, object and subject.

   :param df: A dataframe containing a column 'sentences'.
   :type df: DataFrame
   :param spacy_pipe: Spacy pipe object, given on a function level, because loading it outside the function is more efficient.
   :type spacy_pipe: spacy_pipe

   :returns: *df (DataFrame)* -- A dataframe which only contains sentences with at least one verb, subject and object.


