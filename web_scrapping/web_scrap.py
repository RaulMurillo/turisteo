#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from requests.exceptions import HTTPError
import time
import sys
from bs4 import BeautifulSoup
import logging
from clean_text import *


def get_all_text(url):
    """Retrieves all text in paragraphs.

    :param str url: The URL to scrap.

    :rtype: str :return: Text in the URL.
    """

    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return None
        # sys.exit()
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return None
        # sys.exit()

    soup = BeautifulSoup(response.text, "lxml")

    text = ""
    for i in soup.find_all('p'):  # soup.select
        # i.encode("utf-8") # default
        # Delete citations (e.g. "The Alhambra is a UNESCO World Heritage Site.[2]")
        text += i.get_text() + '\n'

    text = del_nonAscii(del_refs(text))
    return text


def get_text_maxChars(url, maxChars):
    """Retrieves all text in paragraphs up to a limit of characters.

    :param str url: The URL to scrap.    
    :param str maxChars: Maximum number of characters to return.  
    :rtype: str :return: Text in the URL.
    """
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return None
        # sys.exit()
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return None
        # sys.exit()

    soup = BeautifulSoup(response.text, "lxml")

    text = ""
    l_text = 0
    for i in soup.find_all('p'):  # soup.select
        l_paragraph = len(i.text)
        if l_text + l_paragraph > maxChars:
            break
        text += i.get_text() + '\n'
        l_text += l_paragraph + 1

    logging.debug(l_text)
    text = del_nonAscii(del_refs(text))
    return text


def get_entry_text(url):
    """Retrieves text in paragraphs at Wikipedia header.

    :param str url: The URL to scrap.    
    :rtype: str :return: Text in the URL.
    """
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return None
        # sys.exit()
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return None
        # sys.exit()

    soup = BeautifulSoup(response.text, "lxml")
    # This will get the div
    div_container = soup.find('div', class_='mw-parser-output')
    # print(div_container)

    text = ""
    parag = None
    # Get first paragraph
    for child in div_container.children:
        # print(child)
        if ((child.name == 'p') and (len(child) > 1)):
            parag = child
            # print((child.prettify()))
            break

    if parag is None:
        return text
    else:
        text += parag.get_text()  # + '\n'

    # Then search in following contiainers that are paragraphs
    for sibling in parag.next_siblings:
        if sibling.name != 'p':
            break
        # print('Next sibling:', sibling)
        if len(sibling) > 1:
            text += sibling.get_text()  # + '\n'

    text = del_nonAscii(del_refs(text))
    return text


if __name__ == "__main__":
    URL = 'https://en.wikipedia.org/wiki/Alhambra'

    # from google_search import google_search, google_fast_search
    # URL = google_search('Torre ifel', num_res=1, lang='es')[0]
    # URL = google_fast_search('Torre ifel', lang='es')

    print(f'Searching in {URL} ...')
    # print(get_all_text(URL))
    # print(get_text_maxChars(URL, 1000))
    out_text = get_entry_text(URL)

    print(out_text)

    # with open('results_es.txt', 'w') as file:
    #     file.write(out_text)
