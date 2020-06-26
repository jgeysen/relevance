:mod:`relevance.text_cleaning`
==============================

.. py:module:: relevance.text_cleaning

.. autoapi-nested-parse::

   Article cleaning and relevance filtering project
   =========================================================
   The core module of the project



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   relevance.text_cleaning.remove_reuters_lingo
   relevance.text_cleaning.add_spacing
   relevance.text_cleaning.remove_spacing


.. function:: remove_reuters_lingo(article: str) -> str

   Reuters lingo removal function.

   This function cleans the reuters lingo from articles. Reuters articles are written with
   specific linguage and structure. Many symbols with no semantical meaning are being removed.

   :param article: The article that requires cleaning.
   :type article: str

   :returns: *new_article (str)* -- The cleaned article.


.. function:: add_spacing(article: str) -> str

   Add spacing where necessary to the articles.

   This function adds spacing to the article wherever necessary. Reuters articles contain sentences and words which require spacing
   but no spacing is provided. This spacing will processing the article e.g. using sentence splitting functions.

   :param article: The article that requires spacing.
   :type article: str

   :returns: *new_article (str)* -- The article provided with spacing.


.. function:: remove_spacing(article: str) -> str

   Final cleaning, after adding spaces/full stops and removing reuters
   lingo, you end up with double spacing etc. Notice we never reduce the
   number of spaces, this is because we will later filter on spaces to
   recognize tables.

   :param article: The article that requires spacing to be removed.
   :type article: str

   :returns: *new_article (str)* -- The article where spacing has been removed.


