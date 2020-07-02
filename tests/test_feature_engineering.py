from relevance.feature_engineering import preprocess_regex


def test_preprocess_regex() -> None:
    entity_list = ["Aviva"]
    regex_dict = {"Aviva": {"alias": ["Aviva"], "abbrev": ["Aviva"]}}
    all_regex_list = [
        "aviva",
        "[^a-zA-Z]+aviva[^a-zA-Z]+",
        "^aviva[^a-zA-Z]+",
        "[^a-zA-Z]+aviva$",
        "^aviva$",
    ]
    # all_regex_dict = {'alias': ['aviva'], 'abbrev': ['[^a-zA-Z]+aviva[^a-zA-Z]+', '^aviva[^a-zA-Z]+', '[^a-zA-Z]+aviva$', '^aviva$']}
    assert preprocess_regex(entity_list, regex_dict) == all_regex_list
