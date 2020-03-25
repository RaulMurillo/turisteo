#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from playsound import playsound
import os
import requests
import time
from xml.etree import ElementTree
import inflect
import re
import string
import json


try:
    input = raw_input
except NameError:
    pass


class TextToSpeech(object):
    def __init__(self, subscription_key, file, lang):
        languages = {
            'de': ['de-DE', 'KatjaNeural'],
            'en': ['en-US', 'JessaNeural'],
            'es': ['es-ES', 'HelenaRUS'],
            'fr': ['fr-FR', 'HortenseRUS'],
            'it': ['it-IT', 'ElsaNeural']
        }
        self.subscription_key = subscription_key
        self.tts = file
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.language = languages[lang][0]
        self.name = languages[lang][1]

    def get_token(self):
        endpoint_var = 'SPEECH_ENDPOINT'
        if not endpoint_var in os.environ:
            raise Exception(
                'Please set/expot the enviroment variable: {}' .format(endpoint_var))
        fetch_token_url = os.environ[endpoint_var]
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://eastus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'TMI-speech'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set(
            '{http://www.w3.org/XML/1998/namespace}lang', self.language)
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', self.language)
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (' + self.language + ', ' + self.name + ')')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")

        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")


if __name__ == "__main__":
    f = open('text_numbers_letters.txt', 'r', encoding="utf-8")
    file = f.read()
    f.close()
    file_split = file.split()
    if file_split[0] == '[':
        data_string = json.loads(file)
        file = data_string[0]['translations'][0]['text']
        language = data_string[0]['translations'][0]['to']
    else:
        language = 'en'
    key_name = 'SPEECH_SUBCRIPTION_KEY'
    if not key_name in os.environ:
        raise Exception(
            'Please set/expot the enviroment variable: {}' .format(key_name))
    subscription_key = os.environ[key_name]
    app = TextToSpeech(subscription_key, file, language)
    app.get_token()
    app.save_audio()
    time = app.timestr
    playsound('sample-' + time + '.wav')
