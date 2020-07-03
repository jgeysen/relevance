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

   relevance.sentence_splitting.sentence_splitting
   relevance.sentence_splitting.spacy_processing
   relevance.sentence_splitting.nltk_processing
   relevance.sentence_splitting.hasNumbers
   relevance.sentence_splitting.exclude_tables
   relevance.sentence_splitting.parse_short_sentences
   relevance.sentence_splitting.select_actual_sentences


.. function:: sentence_splitting(df: pd.DataFrame) -> pd.DataFrame

   Overarching function which splits reuters articles into sentences,
   optimized for a dataframe.

   This function does the following:

   1. Load spacy and nltk pipes

   2. Call the spacy_processing function on the dataframe to use spacy to split the article into sentences and exclude tables. Parse the resulting sentences back to article level based on the identifier.

   3. Call the nltk_processing function on the articles resulting from step 2 to split the article into sentences. Short sentences are parsed to the nearest longest sentence.

   4. Only selecting those sentences from step 3 which contain at least one subject, object and verb.

   A dataframe containing the sentences resulting from step 4 and their respective article identifier are returned (columns 'sentences' and 'identifier')

   :param df: (pd.DataFrame): A dataframe containing article bodies and article identifiers ('article_body' and 'identifier')

   :returns: *df_sents (pd.DataFrame)* -- A dataframe containing sentences and article identifiers ('sentences' and 'identifier')


.. function:: spacy_processing(df: pd.DataFrame, spacy_pipe: spacy.pipeline) -> pd.DataFrame

   Processing the articles using spacy functionality.

   This function does the following:

   1. Use the spacy sentence splitting model to split the articles into sentences.

   2. Using the 'exclude_tables' functionality in the sentence_splitting module, tables can be differentiated from sentences.

   3. After excluding the tables from the article, the sentences are parsed back together into a processed article body and returned.

   :param df: Dataframe containing a column 'article_body' containing article bodies and a column 'identifier' containing an identifier
   :type df: pd.DataFrame
   :param for each article.:
   :param spacy_pipe: spacy pipe object, called/loaded/passed on a function level for efficiency.
   :type spacy_pipe: spacy.pipeline

   :returns: *df_new (pd.DataFrame)* -- Dataframe containing article body after excluding tables.


.. function:: nltk_processing(df: pd.DataFrame)

   Processing the articles using NLTK.

   This function does the following:

   1. Use the NLTK sentence splitting model to split the article into sentences.

   2. Parse short sentences together with the parse_short_sentences functionality in the sentence_splitting module.

   :param df: Dataframe containing following columns: 'article_body', 'identifier'
   :type df: pd.DataFrame

   :returns: *df_nltk (pd.DataFrame)* -- Dataframe containing following columns: 'sentences', 'identifier'


.. function:: hasNumbers(inputString: str) -> bool

   Check if a string contains numbers function.

   Function which returns true if any character in the inputstring is a digit.

   :param inputString: a string to be checked for containing digits.
   :type inputString: str

   :returns: *Boolean (bool)* -- True if the inputString contains a digit.


.. function:: exclude_tables(df_spacy: pd.DataFrame) -> pd.DataFrame

   Exclude tables function.

   This function excludes tables from an reuters article. Tables aren't sentences, so they are removed.
   If a string meets the following criteria, it's deemed (part of) a table:

   1. The string contains less than 5 actual words (=not containing any digits) AND the sentence contains more than 5 consecutive full stops or spaces

   2. The string has more words containing digits than actual words AND the number of words containing digits is not zero.

   If a 'sentence' meets criteria 1 or 2 (or both), the 'sentence' is removed from the dataframe. It's useful to feed sentences split by spacy to this functionality,
   because spacy splits tables into a number of smaller parts, which can easily be differentiated from actual sentences using these criteria.

   :param df_spacy: pandas dataframe containing the article bodies using column name 'article_body'. No 'identifier' column required because sentences are excluded based on sentence level characteristics. The column containing the sentences has as header 'sentences'. No other column is required.
   :type df_spacy: pd.DataFrame

   :returns: *df_returns (pd.DataFrame)* -- pandas dataframe returning the sentences where words containing digits have been dropped.


.. function:: parse_short_sentences(df_nltk: pd.DataFrame, min_length: int, combination: str) -> pd.DataFrame

   Parse short sentences to long sentences.

   This function parses short sentences with the nearest longer one.

   :param df_nltk: pandas dataframe containing sentences. This dataframe should have the following
   :type df_nltk: pd.DataFrame
   :param columns: sentences, identifier (article level).
   :param min_length: The minimum length of the sentences to be parsed into longer ones.
   :type min_length: int
   :param combination: Can have three values; 'previous' indicating short sentences are parsed with the previous sentence, 'next' indicating short sentences are parsed with the next sentence.
   :type combination: str

   :returns: *df_returns (pd.DataFrame)* -- pandas dataframe containing the sentences after parsing.


.. function:: select_actual_sentences(df: pd.DataFrame, spacy_pipe: spacy.pipeline) -> pd.DataFrame

   Select actual sentences, which contain a verb, subject and object.

   This function uses the spacy dependency labels and selects those sentences which contain a verb, object and subject.

   :param df: A dataframe containing a column 'sentences'. No 'identifier' column required.
   :type df: pd.DataFrame
   :param spacy_pipe: Spacy pipeline object, given on a function level, because loading it once outside the function is more efficient.
   :type spacy_pipe: spacy.pipeline

   :returns: *df (pd.DataFrame)* -- A dataframe which only contains sentences with at least one verb, subject and object.


