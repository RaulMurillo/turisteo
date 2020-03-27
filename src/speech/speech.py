#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from playsound import playsound
import os
import requests
import time
from xml.etree import ElementTree
# import inflect
import re
import string
import json
import logging


try:
    input = raw_input
except NameError:
    pass

languages = {
    'de': ['de-DE', 'KatjaNeural'],
    'en': ['en-US', 'AriaNeural'],
    'es': ['es-ES', 'HelenaRUS'],
    'fr': ['fr-FR', 'HortenseRUS'],
    'it': ['it-IT', 'ElsaNeural'],
    'pt': ['pt-BR', 'FranciscaNeural']
}

class TextToSpeech(object):

    def __init__(self, subscription_key, lang, text=None):
        self.subscription_key = subscription_key
        self.tts = text
        self.timestr = time.strftime(f"%Y%m%d-%H%M%S")
        self.access_token = None
        self.language = languages[lang][0]
        self.name = languages[lang][1]

    def set_lang(self, lang):
        """Set the language of the application.

        lang (str): Must be a valid language code.
        Valid languages are in https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support
        """
        if not lang in languages:
            raise ValueError(
                'Code {} is not a valid language code for speech, please select a valid language code.'.format(lang))
        self.language = languages[lang][0]
        self.name = languages[lang][1]

    def set_text(self, text):
        self.tts = text

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

    def save_audio(self, file_path='./'):
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
            audio_path = file_path + 'sample-' + self.timestr + '.wav'
            with open(audio_path, 'wb') as audio:
                audio.write(response.content)
                logging.info(
                    f"\nStatus code: {response.status_code} \nYour TTS is ready for playback.\n")
            return audio_path

        else:
            logging.error(
                f"\nStatus code: {response.status_code} \nSomething went wrong. Check your subscription key and headers.\n")


if __name__ == "__main__":

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    with open('src/out.txt', 'r', encoding="utf-8") as f:
        in_file = f.read()

    d = json.loads(in_file)
    logging.info(type(d))

    text = d['translations'][0]['text']
    language = d['translations'][0]['to']
    logging.info(language)

    # file_split = in_file.split()
    # if file_split[0] == '[':
    #     data_string = json.loads(in_file)
    #     in_file = data_string[0]['translations'][0]['text']
    #     language = data_string[0]['translations'][0]['to']
    # else:
    #     language = 'en'

    key_name = 'SPEECH_SUBCRIPTION_KEY'
    if not key_name in os.environ:
        raise Exception(
            'Please set/expot the enviroment variable: {}' .format(key_name))
    subscription_key = os.environ[key_name]
    app = TextToSpeech(subscription_key, text, language)
    app.get_token()
    audio = app.save_audio()
    time = app.timestr
    # exit(1)
    playsound(audio)
