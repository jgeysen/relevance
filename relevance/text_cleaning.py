"""
Article cleaning and relevance filtering project
=========================================================
The core module of the project
"""

import re

# the select_text function takes in an article and returns a list of sentences.
# These sentences have been cleaned:
# Removal of reuters lingo.
# Spacing is added in those places where English language would expect spacing.
# Spacing is removed where the English language doesn't expect spacing.

# And checked on:
# Sentences are no pieces of tables:
# They don't contain more than 8 consecutive spaces or full stops.
# They contain more tokens which don't contain digits than tokens which contain digits.
# They are not short: sentences shorter than 10 are parsed with the previous sentence.
# They contain a subject, object and a verb.

# wrapper function for adding spacing and removal of reuters lingo etc.:
# def clean_reuters_article(article):
#     '''
#     Clean articles from reuters - specific reuters artefacts removed
#     Input: article(text)
#     Output: cleaned article (text)
#     '''
#     article1 = remove_reuters_lingo(article)
#     article2 = add_spacing(article1)
#     article3 = remove_spacing(article2)
#     return article3


def remove_reuters_lingo(article: str) -> str:
    """Reuters lingo removal function.

    This function cleans the reuters lingo from articles. Reuters articles are written with
    specific linguage and structure. Many symbols with no semantical meaning are being removed.

    Args:
      article (str): The article that requires cleaning.

    Returns:
      new_article (str): The cleaned article.
    """
    # replace by spacing:
    # Remove company codes, article references and hyperlinks:
    # Everything inbetween < >, less than 30 characters, (company codes).
    # Everything inbetween [ ], less than 30 characters, (company codes and article ref.)
    # Hyperlinks between ( ), shorter than 150 characters.
    spacing_list = [r"<.{0,30}>", r"\[.{0,30}]", r"\(?http\S{0,150}\)?"]
    for regex in spacing_list:
        article = re.sub(regex, "", article)

    new_article = article
    # replace ^>, has no meaning.
    article = re.sub(r"\^\>", "", article)

    # ellipses:
    article = re.sub(r"\.\.\.\s([a-z])", r" \1", article)
    article = re.sub(r"\.\.\.\s([A-Z])", r". \1", article)

    # Replace with full stops:
    # Asterisks: in Reuters data often used to indicate seperate events.
    # >: Also often used to indicate seperate company events.
    full_stop_list = [r"\*", r"\>\>", r"\>", r"-{2,100}"]
    for regex in full_stop_list:
        article = re.sub(regex, r". ", article)

        # Remove reuters lingo at the end of the article:
    remove_list = [
        r"\(Reporting.*\;?\n?.*?\;?\n?.*?\)",  # Any combination of (Reporting by xxxx)
        r"\(\writing.*\n?.*\)",  # Any combination of (Writing by xxxx)
        r"\(\wompiled.*\n?.*\)",  # Any combination of (Compiled by xxxxx)
        r"\(\wditing.*\n?.*\)",  # Any combination of (Editing by xxxxx)
        r"\(Additional.*\n?.*\)",  # Any combination of (Additional xxxxxx)
        r"Source text for Eikon\:",  # Delete 'Source text for Eikon'
        r"For a full report, click on",  # Delete
        r"Further company coverage\:",  # Delete
        r"BLOOMBERG",  # Delete BLOOMBERG
        r"Source text\s?\:",  # Delete 'Source text'
        r"Keywords:",
        r"\(Fixes link to graphic\)",
        r"(Reuters Breakingviews)",
        r"For previous columns by the author, Reuters customers can  click on",
        r"Reuters has not verified\s? these stories and does not vouch for their accuracy\.?",
        r"SIGN UP FOR BREAKINGVIEWS EMAIL ALERTS\.?",
        r"\(?Follow Reuters Summits on Twitter @Reuters_Summits\)?",
        r"\(.{0,20}\sNewsroom:\s.{0,100}\)",  # Any combination of (XXXX Newsroom: XXXX)
        r"\(\$1\s=\s.{0,30}\)",  # Any combination of ($1= XXXX)
        r"\(\s?\(.{0,100}\@.{0,100}\n?.{0,100}?\n?.{0,100}?\)\s?\)",
    ]  # email addresses (of writers etc.) are often mentioned between (( ))

    for regex in remove_list:
        article = re.sub(regex, " ", article)

    # Add a full stop after (Reuters -) (occurs VERY often at the start of the article):
    new_article = re.sub(r"\(Reuters\)\s\-", r"(Reuters) -. ", article)

    return new_article


def add_spacing(article: str) -> str:
    """Add spacing where necessary to the articles.

    This function adds spacing to the article wherever necessary. Reuters articles contain sentences and words which require spacing
    but no spacing is provided. This spacing will processing the article e.g. using sentence splitting functions.

    Args:
      article (str): The article that requires spacing.

    Returns:
      new_article (str): The article provided with spacing.
    """
    # Add space after the word 'premarket' and 'pct' (occurs often without spacing):
    article = re.sub(r"premarket", r"premarket ", article)
    article = re.sub(r"pct", r"pct ", article)

    # Replace a full stop followed by a dash by full stop.
    article = re.sub(r"\.\-", r".", article)

    # Add a whitespace when a numerical character is mentioned without spacing: 'abc2013abc' -> 'abc 2013 abc'
    # if e.g. '1.2 billion' is mentioned, this shouldn't change!
    article = re.sub(r"([a-z]+)([0-9]+(\.[0-9]+)?(\,[0-9]+)?\.?)", r"\1 \2", article)
    article = re.sub(r"([0-9]+(\.[0-9]+)?(\,[0-9]+)?\.?)([a-z]+)", r"\1 \4", article)

    # Add spaces before and after parentheses,
    # except when after the parentheses there is any kind of punctuation.
    article = re.sub(r"(\w+)(\()", r"\1 \2", article)
    article = re.sub(r"(\)\.?\,?\;?\??\!?)(\w+)", r"\1 \2", article)

    # the same for square brackets.
    article = re.sub(r"(\w+)(\[)", r"\1 \2", article)
    article = re.sub(r"(\]\.?\,?\;?\??\!?)(\w+)", r"\1 \2", article)

    # Add whitespace when ' ." ' occurs.
    # Add whitespace when ' ". ' occurs.
    # Add whitespace when 'abc.Abc' occurs.
    # Add whitespace when 'ABC.Abc' occurs.
    # Add whitespace when 'abc.ABC' occurs.
    article = re.sub(r"(\.)(\"\w+)", r"\1 \2", article)
    article = re.sub(r"(\w+\"\.)(\w+)", r"\1 \2", article)
    article = re.sub(r"([A-Z]+\.)([A-Z][a-z])", r"\1 \2", article)
    article = re.sub(r"([a-z]+\.)([A-Z][a-z]+)", r"\1 \2", article)
    article = re.sub(r"([a-z]+\.)([A-Z]+)", r"\1 \2", article)
    article = re.sub(r"(\.)(\<)", r"\1 \2", article)

    # colon: add whitespace when 'abc:abc' occurs.
    article = re.sub(r"(\w+?\:)(\"?\w+)", r"\1 \2", article)

    # semicolon: add whitespace when 'abc;abc' occurs.
    new_article = re.sub(r"(\w+?\;)(\"?\w+)", r"\1 \2", article)

    return new_article


## Add a whitespace when a numerical character is mentioned without spacing: 'abc2013abc'.
## Some final cleaning, removal of redundant spacing.


def remove_spacing(article: str) -> str:
    """Final cleaning, after adding spaces/full stops and removing reuters
    lingo, you end up with double spacing etc. Notice we never reduce the
    number of spaces, this is because we will later filter on spaces to
    recognize tables.

    Args:
      article (str): The article that requires spacing to be removed.

    Returns:
      new_article (str): The article where spacing has been removed.
    """
    article = re.sub(r"\^", r"", article)
    article = re.sub(r"\¬", r" ", article)
    article = re.sub(r"\¨", r" ", article)
    article = re.sub(r"\:\.", r":", article)
    article = re.sub(r"\s\,", r",", article)
    article = re.sub(r"\s\:", r":", article)
    article = re.sub(r"\s\;", r";", article)
    clean1 = [r"\.\.", r"\.\s\s\.", r"\.\s\.", r"\s\s\.", r"\s\."]
    for regex in clean1:
        article = re.sub(regex, r".", article)

    new_article = article
    return new_article
