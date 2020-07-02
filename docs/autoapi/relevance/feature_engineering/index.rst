:mod:`relevance.feature_engineering`
====================================

.. py:module:: relevance.feature_engineering

.. autoapi-nested-parse::

   Article cleaning and relevance filtering project
   =========================================================
   The core module of the project



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   relevance.feature_engineering.preprocess_regex


.. function:: preprocess_regex(entity_list: list, regex_dict: dict)

   Preprocess the regexes.

   This function parses the regexes and abbreviations given as strings into regexes.
   Entity list contains the entities, which one wants to find the relevant content for. The dictionary contains both the abbreviations and aliases for each of these entities.
   For example:
   The name 'Aviva', should match every occurence of Aviva. As we know, Reuters articles (or any other source), can be noisy. Words can be added before or after an occurence
   of 'Aviva', e.g. 'Avivahas published it's quarterly numbers'.

   preprocess_regex returns all regexes for both abbreviations and aliases for the entities in entity_list which will match with noisy mentions of these entities.

   :param entity_list: List of entity names.
   :type entity_list: list
   :param regex_dict: Dictionary which has as a key the entity name and 'alias' and 'abbrev'. For each entity, this dictionary contains a list of aliases and abbreviations.
   :type regex_dict: dict

   :returns: *all_regex_list (list)* -- List of all regexes.
             all_regex_dict (dict): Dictionary of all aliases and abbrevations. This dictionary contains two keys: 'alias' and 'abbrev'.


