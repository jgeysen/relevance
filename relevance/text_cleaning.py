"""
Article cleaning and relevance filtering project
=========================================================
The core module of the project
"""

import re

# the select_text function takes in an article and returns a list of sentences.
## These sentences have been cleaned:
### Removal of reuters lingo.
### Spacing is added in those places where English language would expect spacing.
### Spacing is removed where the English language doesn't expect spacing.

## And checked on:
## Sentences are no pieces of tables:
### They don't contain more than 8 consecutive spaces or full stops.
### They contain more tokens which don't contain digits than tokens which contain digits.
## They are not short: sentences shorter than 10 are parsed with the previous sentence.
## They contain a subject, object and a verb.

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

    This function cleans the reuters lingo from articles.

    Args:
      article (str): The article that requires cleaning.

    Returns:
      new_article (str): The cleaned article.
    """
    # replace by spacing:
    # Remove company codes, article references and hyperlinks:
    ## Everything inbetween < >, less than 30 characters, (company codes).
    ## Everything inbetween [ ], less than 30 characters, (company codes and article ref.)
    ## Hyperlinks between ( ), shorter than 150 characters.
    spacing_list = [r"<.{0,30}>", r"\[.{0,30}]"]  # , "\(?http\S{0,150}\)?"]
    for regex in spacing_list:
        article = re.sub(regex, "", article)

    new_article = article
    # # replace ^>, has no meaning.
    # article = re.sub("\^\>", "", article)

    # # ellipses:
    # article = re.sub("\.\.\.\s([a-z])", " \1", article)
    # article = re.sub(r"\.\.\.\s([A-Z])", r". \1", article)

    # # Replace with full stops:
    # ## Asterisks: in Reuters data often used to indicate seperate events.
    # ## >: Also often used to indicate seperate company events.
    # full_stop_list = ["\*", "\>\>", "\>", "-{2,100}"]
    # for regex in full_stop_list:
    #     article = re.sub(regex, ". ", article)

    # # Remove reuters lingo at the end of the article:
    # remove_list = [
    #     "\(Reporting.*\;?\n?.*?\;?\n?.*?\)",  ## Any combination of (Reporting by xxxx)
    #     "\(\writing.*\n?.*\)",  ## Any combination of (Writing by xxxx)
    #     "\(\wompiled.*\n?.*\)",  ## Any combination of (Compiled by xxxxx)
    #     "\(\wditing.*\n?.*\)",  ## Any combination of (Editing by xxxxx)
    #     "\(Additional.*\n?.*\)",  ## Any combination of (Additional xxxxxx)
    #     "Source text for Eikon\:",  ## Delete 'Source text for Eikon'
    #     "For a full report, click on",  # Delete
    #     "Further company coverage\:",  # Delete
    #     "BLOOMBERG",  ## Delete BLOOMBERG
    #     "Source text\s?\:",  ## Delete 'Source text'
    #     "Keywords:",
    #     "\(Fixes link to graphic\)",
    #     "(Reuters Breakingviews)",
    #     "For previous columns by the author, Reuters customers can  click on",
    #     "Reuters has not verified\s? these stories and does not vouch for their accuracy\.?",
    #     "SIGN UP FOR BREAKINGVIEWS EMAIL ALERTS\.?",
    #     "\(?Follow Reuters Summits on Twitter @Reuters_Summits\)?",
    #     "\(.{0,20}\sNewsroom:\s.{0,100}\)",  ## Any combination of (XXXX Newsroom: XXXX)
    #     "\(\$1\s=\s.{0,30}\)",  ## Any combination of ($1= XXXX)
    #     "\(\s?\(.{0,100}\@.{0,100}\n?.{0,100}?\n?.{0,100}?\)\s?\)",
    # ]  ## email addresses (of writers etc.) are often mentioned between (( ))

    # for regex in remove_list:
    #     article = re.sub(regex, " ", article)

    # # Add a full stop after (Reuters -) (occurs VERY often at the start of the article):
    # new_article = re.sub("\(Reuters\)\s\-", "(Reuters) -. ", article)

    return new_article
