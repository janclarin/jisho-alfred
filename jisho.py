#!/usr/bin/env python
# encoding: utf-8

import sys
from workflow import Workflow, web, ICON_WEB

API_URL = 'http://jisho.org/api/v1/search/words'
SEP_COMMA = u'、 '   # Separator for subtitle kana readings.
MAX_NUM_RESULTS = 9  # Maximum number of results that Alfred can display.


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
    japanese_info = result['japanese']

    # Prefer kanji as title over kana.
    if 'word' in japanese_info[0]:
        title = japanese_info[0]['word']
        subtitle = combine_kana_readings(japanese_info)
    else:
        title = japanese_info[0]['reading']
        # Ignore first reading since it was used as the title.
        subtitle = combine_kana_readings(japanese_info[1:])

    wf.add_item(title=title,
                subtitle=subtitle,
                arg=title,
                valid=True,
                largetext=title,
                icon=ICON_WEB)


def combine_kana_readings(japanese_info):
    """Combines the kana readings for the japanese info with the SEP_COMMA.
    Args:
        japanese_info: An array with dict elements with reading info.
    """
    return SEP_COMMA.join([word['reading'] for word in japanese_info])


def main(wf):
    """Main function to handle query and request info from Jisho.org.
    Args:
        wf: An instance of Workflow.
    """
    # Get query from Alfred.
    query = wf.args[0] if len(wf.args) else None

    # Retrieve results from Jisho.org.
    results = get_results(query)

    # Add results, up to the maximum number of results, to Alfred.
    for i in range(min(len(results), MAX_NUM_RESULTS)):
        add_alfred_result(wf, results[i])

    # Send the results to Alfred as XML.
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
