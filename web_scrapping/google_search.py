# -*- coding: utf-8 -*-
# https://www.geeksforgeeks.org/performing-google-search-using-python-code/
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def google_search(query, lang='en', num_res=5):
    """Returns the URLs that result of a Google query.

    :param str query: The Google query.    
    :param str lang: Languaje of the query.   
    :param int num_res: Number of URLs to return.       
    :rtype: list :return: List with URLs.
    """
    # website
    site = f'site:{lang}.wikipedia.org'  # site:wikipedia.org
    # print(f'{site} {query}')

    results = []
    for j in search(f'{site} {query}', tld="com", lang=lang, num=10, stop=num_res, pause=1.0):
        # print(j)
        results.append(j)
    return results


def google_fast_search(query, lang='en'):
    """Returns the first URL that results of a Google query.

    :param str query: The Google query.    
    :param str lang: Languaje of the query.     
    :rtype: str :return: URL.
    """
    # website
    site = f'site:{lang}.wikipedia.org'  # site:wikipedia.org
    # print(f'{site} {query}')

    # Search only for Google's first result
    for r in search(f'{site} {query}', tld="com", lang=lang, num=1, stop=1, pause=0.0):
        return r


if __name__ == "__main__":
    # to search
    query = "Alhambra"

    print(google_search(query, num_res=1))
