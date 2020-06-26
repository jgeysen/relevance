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


.. function:: hasNumbers(inputString: str) -> bool

   Check if a string contains numbers function.

   Function which returns true if there's a digit in the inputstring.

   :param inputString: a string
   :type inputString: str

   :returns: *Boolean (bool)* -- True if the inputString contains a digit.


.. function:: exclude_tables(df_spacy: pd.DataFrame) -> pd.DataFrame

   Exclude tables function.

   This function excludes tables from an reuters article. Tables are not sentences, so they can/have to be removed.

   :param df_spacy: pandas dataframe containing the articles. The column containing the sentences has as header 'sentences'.
   :type df_spacy: DataFrame

   :returns: *df_returns (DataFrame)* -- pandas dataframe returning the sentences where words containing digits have been dropped.


