from relevance.text_cleaning import (
    add_spacing,
    clean_reuters_article,
    remove_reuters_lingo,
    remove_spacing,
)


def test_remove_reuters_lingo() -> None:
    article = r"Reuters articles contain a lot of noise * Asterisks are used to indicate ends of sentences or even more exotic things >> Additinoally the articles can contain hyperlinks betwen brackets (https:\\www.reuters.com\). BLOOMBERG Further company coverage: (Follow Reuters Summits on Twitter @Reuters_Summits)."
    clean_article = "Reuters articles contain a lot of noise .  Asterisks are used to indicate ends of sentences or even more exotic things .  Additinoally the articles can contain hyperlinks betwen brackets       ."
    assert remove_reuters_lingo(article) == clean_article


def test_add_spacing() -> None:
    article = "This is a test article with some deliberate mistakes towards spacing.Spaces have been leftout after fullstops,afer commas and after colons:This way we're sure the functionality picks up on those mistakes.This package has been developed in2020.There are 6.8billion people in te world."
    clean_article = "This is a test article with some deliberate mistakes towards spacing. Spaces have been leftout after fullstops,afer commas and after colons: This way we're sure the functionality picks up on those mistakes. This package has been developed in 2020. There are 6.8 billion people in te world."
    assert add_spacing(article) == clean_article


def test_remove_spacing() -> None:
    article = "There shouldn't be spaces before commas , as there shouldn't be spaces before colons : or semi colons ; these are checked here ."
    clean_article = "There shouldn't be spaces before commas, as there shouldn't be spaces before colons: or semi colons; these are checked here."
    assert remove_spacing(article) == clean_article


def test_clean_reuters_article() -> None:
    article = r"This is a test article with some deliberate mistakes towards spacing.Spaces have been leftout after fullstops,afer commas and after colons:This way we're sure the functionality picks up on those mistakes.This package has been developed in2020.There are 6.8billion people in te world. There shouldn't be spaces before commas , as there shouldn't be spaces before colons : or semi colons ; these are checked here . Reuters articles contain a lot of noise * Asterisks are used to indicate ends of sentences or even more exotic things >> Additionally the articles can contain hyperlinks betwen brackets (https:\\www.reuters.com\). BLOOMBERG Further company coverage: (Follow Reuters Summits on Twitter @Reuters_Summits)."
    clean_article = "This is a test article with some deliberate mistakes towards spacing. Spaces have been leftout after fullstops,afer commas and after colons: This way we're sure the functionality picks up on those mistakes. This package has been developed in 2020. There are 6.8 billion people in te world. There shouldn't be spaces before commas, as there shouldn't be spaces before colons: or semi colons; these are checked here. Reuters articles contain a lot of noise.  Asterisks are used to indicate ends of sentences or even more exotic things.  Additionally the articles can contain hyperlinks betwen brackets    ."
    assert clean_reuters_article(article) == clean_article
