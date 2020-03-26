#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import requests
import uuid
import json
import csv

subscription_key = None
endpoint = None
MAX_LENGTH = 2500


def check_credentials():
    key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
    if not key_var_name in os.environ:
        raise Exception(
            'Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
    if not endpoint_var_name in os.environ:
        raise Exception(
            'Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    return (subscription_key, endpoint)


def split(text):
    s = []
    if len(text) > MAX_LENGTH:
        pos = 0
        for i in text:
            if i == "\n":
                break
            pos += 1
        s.append(text[:pos])

        if(text[pos + 1:] != ''):
            s += split(text[pos + 1:])
    else:
        s.append(text)
    return s


def translate(text_input, lang='es', orig=None):
    """Translate a text into a given language.

    Parameters: 
        text_input (str): The text to be translated.
        lang (str): The target languaje to translate the text.
        orig (str): Origin languaje of text `text_input`.
    Returns:
        dict: Equivalent to JSON with the translated text.
    """
    subscription_key, endpoint = check_credentials()

    if len(text_input) > MAX_LENGTH:
        texts = text_input.splitlines(True)
        for i, t in enumerate(texts):
            if len(t) > MAX_LENGTH:
                paragraph = t.split('.')
                texts = texts[:i] + paragraph + texts[i+1:]
    else:
        texts = [text_input]

    path = '/translate?api-version=3.0'
    params = '&to='+lang
    if orig:
        params += '&from='+orig
    constructed_url = endpoint + path + params

    response = [None] * len(texts)
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    for i, text in enumerate(texts):

        body = [
            {"text": text}  # max size
        ]

        request = requests.post(constructed_url, headers=headers, json=body)
        response[i] = request.json()[0]

    for r in response[1:]:
        response[0]['translations'][0]['text'] += r['translations'][0]['text']

    # out_json = json.dumps(response[0], ensure_ascii=False,
    #                  sort_keys=True, indent=4, separators=(',', ': '))
    # with open("src/out.txt", "w") as f:
    #     f.write(out_json)

    return response[0]


if __name__ == '__main__':
    # Example
    with open("src/text.txt", "r") as f:
        r = f.read()

    translate(r)
    # translate(r, lang='pt', orig='en')
    #output: out.txt
