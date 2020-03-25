#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import time
import sys


if __name__ == "__main__":
    query = "alhambra"
    query = query.replace(' ', '+')
    site = 'site:en.wikipedia.org'
    URL = f"https://google.com/search?q={site}+{query}"

    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    headers = {"user-agent": USER_AGENT}

    try:
        response = requests.get(URL, headers=headers)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        # return None
        sys.exit()
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        # return None
        sys.exit()

    soup = BeautifulSoup(response.text, "lxml")
    # print(soup)
    # exit(1)

    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('axdfgh')
        if anchors:
            link = anchors[0]['href']
            # title = g.find('h3').text
            item = {
                # "title": title,
                "link": link
            }
            results.append(item)
    print(results)
