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

   relevance.text_cleaning.clean_reuters_article
   relevance.text_cleaning.remove_reuters_lingo
   relevance.text_cleaning.add_spacing
   relevance.text_cleaning.remove_spacing


.. function:: clean_reuters_article(article: str) -> str

   Wrapper function which calls all functions in the module.

   Clean articles from reuters - specific reuters artefacts are removed: reuters lingo is removed,
   spacing is added where necessary and spacing is removed where unnecessary.

   :param article: The article to be cleaned.
   :type article: str

   :returns: *article3 (str)* -- The article which is cleaned.


.. function:: remove_reuters_lingo(article: str) -> str

   Reuters lingo removal function.

   This function cleans the reuters lingo from articles. Reuters articles are written with
   specific language and structure. Many symbols with no semantical meaning are being removed.

   :param article: The article that requires cleaning.
   :type article: str

   :returns: *new_article (str)* -- The cleaned article.


.. function:: add_spacing(article: str) -> str

   Add spacing where necessary to the articles.

   This function adds spacing to the article wherever necessary: adding spacing where it belongs according to the rules of the English language, e.g.
   a space after a full stop: "abc:abc" -> "abc: abc", a space after a comma: "abc,abc" -> "abc, abc", etc.

   The implemented rules use regexes to only add spacing
   only where it is required. Reuters articles are noisy
   and require spacing where no spacing is provided. This spacing will help processing the article e.g. using
   sentence splitting functions.

   :param article: The article that requires spacing.
   :type article: str

   :returns: *new_article (str)* -- The article provided with spacing in the right locations.


.. function:: remove_spacing(article: str) -> str

   Function to remove unnecessary spacing from articles.

   Reuters articles are noisy and contain often contain spacing in undesirable locations.
   This spacing will confuse any further processing of the article e.g. using
   sentence splitting functions.

   Notice we never reduce the
   number of consecutive spaces (e.g. reducing 5 consecutive spaces by 1),
   this is because we will later filter on spaces to recognize tables.

   :param article: The article that requires spacing to be removed.
   :type article: str

   :returns: *new_article (str)* -- The article where spacing has been removed.


