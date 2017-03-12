#!/usr/bin/env python
# encoding: utf-8

import sys
from itertools import chain
from workflow import Workflow, web, ICON_WEB, ICON_INFO

API_URL = 'http://jisho.org/api/v1/search/words'
MAX_NUM_RESULTS = 9  # Maximum number of results that Alfred can display.
SEP_COMMA = u'、 '   # Separator between Japanese characters and words.
SEP_BAR = u' | '     # Separator between different info: kana and definitions.


def get_results(query):
    """Fetches query search results from Jisho.org API.
    Args:
        query: A string representing the search query for Jisho.org.
    Returns:
        An array of JSON results from Jisho.org based on search query.
    """
    params = dict(keyword=query)
    request = web.get(API_URL, params)

    # Throw an error if request failed.
    request.raise_for_status()

    # Parse response as JSON and extract results.
    response = request.json()
    return response['data']


def add_alfred_result(wf, result):
    """Adds the result to Alfred.
    Args:
        wf: An instance of Workflow.
        result: A dict representation of info about the Japanese word.
    """
    # Contains kanji and kana for the result.
    japanese = result['japanese']

    # Contains info like English definitions and parts of speech.
    senses = result['senses']

    # Get Alfred result item information.
    title = get_title(japanese)
    subtitle = get_subtitle(japanese, senses)
    url_arg = get_url_arg(japanese)

    # Add Alfred result item based on info above.
    wf.add_item(title=title, subtitle=subtitle, arg=url_arg, valid=True,
                largetext=title, icon=ICON_WEB)


def has_kanji(japanese):
    """Returns True if there is at least one kanji/word for the term.
    Args:
        japanese: An array with dict elements with reading info from Jisho.
    Returns:
        True if there is a kanji/word for a term.
    """
    return any(['word' in word_reading for word_reading in japanese])


def get_title(japanese):
    """Creates a string with kanji or kana if there is no kanji.
    Args:
        japanese: An array with dict elements with reading info from Jisho.
    Returns:
        A string with kanji or kana if there is no kanji.
    """
    if has_kanji(japanese):
        return combine_japanese_field(japanese, 'word')
    else:
        return combine_japanese_field(japanese, 'reading')


def get_subtitle(japanese, senses):
    """Creates a string with the kana (if a kanji term) and english definitions.
    Args:
        japanese: An array with dict elements with reading info from Jisho.
        senses: An array with dict elements with English info.
    Returns:
        A string with kana readings and English definitions if available.
    """
    combined_eng_defs = combine_english_defs(senses)
    subtitle = u''

    if has_kanji(japanese):
        combined_kana_readings = combine_japanese_field(japanese, 'reading')

        # Try to combine kana readings and English definitions if both exist.
        if combined_kana_readings and combined_eng_defs:
            subtitle = combined_kana_readings + SEP_BAR + combined_eng_defs
        elif combined_kana_readings:
            subtitle = combined_kana_readings
        elif combined_eng_defs:
            subtitle = combined_eng_defs
    else:
        # Just English definitions if not kana, kana probably used for title.
        subtitle = combined_eng_defs

    return subtitle


def get_url_arg(japanese):
    """Gets the first kanji or kana reading for searching in Jisho for a result.

    Used when pressing 'Enter' on an Alfred result. This arg is the term that
    will be used as the search term on jisho.org.

    Args:
        japanese: An array with dict elements with reading info from Jisho.
    Returns:
        A string representing kanji or a kana term to search for in browser.
    """
    if has_kanji(japanese):
        return japanese[0]['word']
    else:
        return japanese[0]['reading']


def combine_japanese_field(japanese, field, separator=SEP_COMMA):
    """Combines unique kanji/kana readings for japanese.
    Args:
        japanese: An array with dict elements with reading info from Jisho.
        field: A string representing the field in japanese, 'word' or 'reading'
    Returns:
        A string of Japanese kanji or kana separated by the separator.
    """
    japanese_words = {word[field] for word in japanese if field in word}
    return separator.join(japanese_words)


def combine_english_defs(senses, separator=u', '):
    """Combines the English definitions in senses.
    Args:
        senses: An array with dict elements with English info.
    Returns:
        A string of English definitions separated by the separator.
    """
    # Each sense contains a list of English definitions. e.g. [[], [], []]
    eng_defs_lists = [sense['english_definitions'] for sense in senses
                      if 'english_definitions' in sense]

    # Combine the inner lists of English definitions into one list.
    combined_eng_defs = chain.from_iterable(eng_defs_lists)
    return separator.join(combined_eng_defs)


def is_valid_query(query):
    """Returns True if the query is not just a single quote.
    Args:
        query: A string representing the search query for Jisho.org.
    Returns:
        True if the query is not just a single- or double-quotation mark.
    """
    sanitized_query = query.strip()
    return not (sanitized_query == u'"' or sanitized_query == u"'")


def main(wf):
    """Main function to handle query and request info from Jisho.org.
    Args:
        wf: An instance of Workflow.
    """
    # Get query from Alfred.
    query = wf.args[0] if len(wf.args) else None

    # Only fetch results if it is a valid query.
    if not is_valid_query(query):
        return

    # Add query result if there is an update.
    if wf.update_available:
        wf.add_item('A newer version of Jisho Alfred Workflow is available',
                    'Action this item to download and install the new version',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    # Retrieve results from Jisho.org.
    results = get_results(query)

    # Add results, up to the maximum number of results, to Alfred.
    for i in range(min(len(results), MAX_NUM_RESULTS)):
        add_alfred_result(wf, results[i])

    # Send the results to Alfred as XML.
    wf.send_feedback()

if __name__ == '__main__':
    # Initialize and configure workflow to self-update.
    wf = Workflow(update_settings={
        'github_slug': 'janclarin/jisho-alfred-workflow'
    })
    sys.exit(wf.run(main))
