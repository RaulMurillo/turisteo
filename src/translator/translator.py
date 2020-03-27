#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import requests
import uuid
import json
# import csv


class TranslatorText:
    def __init__(self, subscription_key, text, lang, orig=None):
        self._subscription_key = subscription_key
        self._ttt = text     # Text to translate
        self._language = lang
        self._origin = orig
        self._MAX_LENGTH = 2500

    def set_lang(self, lang, orig):
        self._language = lang
        self._origin = orig

    def set_text(self, text):
        self._ttt = text

    def split(self):
        """ Split a long text on paragraphs, or lines if needed. """
        paragraphs = self._ttt.splitlines(keepends=True)
        for i, p in enumerate(paragraphs):
            if len(p) > self._MAX_LENGTH:
                # Split in lines
                lines = p.split('. ')
                lines = [l + '. ' for l in lines]
                paragraphs = paragraphs[:i] + lines + paragraphs[i+1:]
        return paragraphs

    def translate(self):
        """Translate the text into the given language."""
        endpoint_var = 'TRANSLATOR_TEXT_ENDPOINT'
        if not endpoint_var in os.environ:
            raise Exception(
                'Please set/export the environment variable: {}'.format(endpoint_var))
        endpoint = os.environ[endpoint_var]

        if len(self._ttt) > self._MAX_LENGTH:
            trad_in = self._split()
        else:
            trad_in = [self._ttt]

        path = '/translate?api-version=3.0'
        params = '&to='+self._language
        if self._origin:
            params += '&from='+self._origin
        constructed_url = endpoint + path + params
        headers = {
            'Ocp-Apim-Subscription-Key': self._subscription_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        response = [requests.post(constructed_url, headers=headers, json=[
                                  {"text": text}]).json()[0] for text in trad_in]

        for r in response[1:]:
            response[0]['translations'][0]['text'] += r['translations'][0]['text']

        return response[0]


if __name__ == '__main__':
    # Example
    with open("text.txt", "r") as f:
        text = f.read()

    key_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
    if not key_name in os.environ:
        raise Exception(
            'Please set/expot the enviroment variable: {}' .format(key_name))
    subscription_key = os.environ[key_name]

    app = TranslatorText(subscription_key, text, lang='es')
    traduction = app.translate()
    print(traduction)
    print()
    app.set_lang(lang='pt', orig='en')
    print(app.translate())
