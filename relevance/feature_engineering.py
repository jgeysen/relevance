"""
Article cleaning and relevance filtering project
=========================================================
The core module of the project
"""
# import packages


# feature engineering

# def create_comb_features_target(df,regex_dict,entity_list):
#     # create all combinations (of any length) of entities in the entity list:
#     combo_list = list(itertools.chain.from_iterable([itertools.combinations(entity_list,i) for i in range(1,len(entity_list)+1)]))
#     combo_list = [list(i) for i in combo_list]
#     # initialize a dataframe to store all intermediate dataframes:
#     df_final = pd.DataFrame()
#     # loop over all combinations:
#     for combo in combo_list:
#         # for one combination of companies, create features:
#         df_data,all_regex_dict,feature_list = create_features_target1(df,regex_dict,combo)
#         # put the regexes used to create this specific subset in an additional column:
#         regex_info = pd.Series([all_regex_dict]*len(df_data),name='regexes')
#         # concatenate everything:
#         df_data = pd.concat([df_data,regex_info],axis=1)
#         df_final = pd.concat([df_final,df_data],axis=0)
#     return df_final.reset_index(drop=True),feature_list

# def create_features_target(df,regex_dict,entity_list):
#     all_regex_list,all_regex_dict = preprocess_regex(entity_list,regex_dict)
#     # create features
#     df,feature_list = create_features(df,all_regex_list)
#     # create targets
#     df['target'] = df[entity_list].max(axis=1).fillna(0)
#     # new dataframe both containing targets and features:
#     df_data = pd.concat([df[feature_list],df['target']],axis=1,sort=False).reset_index(drop=True)
#     # return
#     return df_data,all_regex_dict,feature_list

# def create_features_no_target(df,regex_dict,entity_list):
#     all_regex_list,all_regex_dict = preprocess_regex(entity_list,regex_dict)
#     # create features
#     df_data,feature_list = create_features(df,all_regex_list)
#     # new dataframe both containing targets and features:
#     df_data = df_data.reset_index(drop=True)
#     # return
#     return df_data,all_regex_dict,feature_list

# def create_features(df: pd.DataFrame,regex_list: list) -> :
#     feature_list = []

#     # add a position column to the dataframe, which describes the sentence position in the article:
#     df['position'] = 1
#     df['position'] = df.groupby(['identifier'],sort=False)['position'].transform(pd.Series.cumsum)

#     # Length of the aritcle (absolute, number of sentences)
#     # already created, df['total_length']
#     feature = 'total_length1'
#     art_lengths = pd.DataFrame(df.groupby(['identifier'],sort=False).size(),columns=[feature]).reset_index(drop=False)
#     df = pd.merge(df, art_lengths, on="identifier")
#     feature_list += ['total_length1']

#     # company name mentioned in sentence:
#     regex = '|'.join(regex_list)
#     feature = 'entity_mention'
#     df[feature] = df.sentences.str.lower().str.contains(regex,regex=True)
#     df[feature] = [1 if x is True else 0 for x in df[feature].tolist()]
#     feature_list += [feature]

#     # ## print words in articles containing entity name
#     # print('The following combinations of the abbreviations were used to match the entitities:')
#     # print('\n')
#     # entity_tokens = []
#     # for sent in df[df['entity_mention']==1].sentences:
#     #     tokens = sent.split(' ')
#     #     entity_tokens += [token.lower() for token in tokens if bool(re.search(regex,token.lower())) == True]
#     # print(set(entity_tokens))
#     # print('\n')

#     # company name mentioned in previous sentence/next sentence(s)
#     x = 10
#     for i in range(1,x+1):
#         feature = 'entity_mention_' + str(i) + '_sentence_earlier'
#         df[feature] = df.groupby(['identifier'],sort=False)['entity_mention'].shift(i,fill_value=0)
#         feature_list += [feature]

#         feature = 'entity_mention_' + str(i) + '_sentence_later'
#         df[feature] = df.groupby(['identifier'],sort=False)['entity_mention'].shift(-i,fill_value=0)
#         feature_list += [feature]

#     # Company name mentioned in the title:
#     feature = 'title_mention'
#     regex = '|'.join(regex_list)
#     df[feature] = df.identifier.str.lower().str.contains(regex,regex=True)
#     # depending which identifier is used, use the title or the identifier if the
#     # title is used as identifier (not ideal).
#     #df[feature] = df.title.str.lower().str.contains(regex,regex=True)
#     df[feature] = [1 if x is True else 0 for x in df[feature].tolist()]
#     feature_list += [feature]

#     # Position of the sentence in the article (sentence position/article sent length):
#     feature = 'rel_position_in_art'
#     df[feature] = df['position'].values/df['total_length1'].values
#     feature_list += [feature]

#     # Length of the sentence (characters):
#     feature = 'sent_length_char'
#     df[feature] = df.sentences.str.len()
#     feature_list += [feature]

#     # Length of the sentence (tokens/words):
#     feature = 'sent_length_words'
#     df[feature] = [len(x.split(' ')) for x in df.sentences]
#     feature_list += [feature]

#     return df,feature_list


def preprocess_regex(entity_list: list, regex_dict: dict):
    """Preprocess the regexes.

    This function parses the regexes and abbreviations given as strings into regexes.
    Entity list contains the entities, which one wants to find the relevant content for. The dictionary contains both the abbreviations and aliases for each of these entities.
    For example:
    The name 'Aviva', should match every occurence of Aviva. As we know, Reuters articles (or any other source), can be noisy. Words can be added before or after an occurence
    of 'Aviva', e.g. 'Avivahas published it's quarterly numbers'.

    preprocess_regex returns all regexes for both abbreviations and aliases for the entities in entity_list which will match with noisy mentions of these entities.

    Args:
        entity_list (list): List of entity names.
        regex_dict (dict): Dictionary which has as a key the entity name and 'alias' and 'abbrev'. For each entity, this dictionary contains a list of aliases and abbreviations.

    Returns:
        all_regex_list (list): List of all regexes.
        all_regex_dict (dict): Dictionary of all aliases and abbrevations. This dictionary contains two keys: 'alias' and 'abbrev'.
    """
    # create lists for both aliases and abbreviations, create regexes from each element in these lists.
    # return it all.
    all_alias = []
    all_abbrev = []
    for entity in entity_list:
        all_alias += regex_dict[entity]["alias"]
        all_abbrev += regex_dict[entity]["abbrev"]
    # all_alias_regex,all_abbrev_regex = create_regex(all_alias,all_abbrev)
    # lowercase both aliases and replace spaces with optional space regex '\s?':
    all_alias_regex = [
        r"\s?".join(alias.lower().split(" ")) for alias in all_alias if len(alias) > 0
    ]
    # add regex combinations to abbreviations; everything except alphabetical characters in front and after:
    abbrev_regex1 = [
        "[^a-zA-Z]+" + abbrev.lower() + "[^a-zA-Z]+" for abbrev in all_abbrev
    ]
    # the sentence can start with the abbrev:
    abbrev_regex2 = ["^" + abbrev.lower() + "[^a-zA-Z]+" for abbrev in all_abbrev]
    # the sentence can end with the abbrev:
    abbrev_regex3 = ["[^a-zA-Z]+" + abbrev.lower() + "$" for abbrev in all_abbrev]
    # the sentence can only consist of the abbrev (mainly for printing the substrings):
    abbrev_regex4 = ["^" + abbrev.lower() + "$" for abbrev in all_abbrev]
    # append abbreviation regexes:
    all_abbrev_regex = abbrev_regex1 + abbrev_regex2 + abbrev_regex3 + abbrev_regex4
    # append to list:
    all_regex_list = all_alias_regex + all_abbrev_regex
    # append to dictionary:
    all_regex_dict = {"alias": all_alias_regex, "abbrev": all_abbrev_regex}

    return all_regex_list, all_regex_dict
