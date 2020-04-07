#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# from playsound import playsound
from app import app
import os
import requests
import time
from xml.etree import ElementTree
# import inflect
# import re
# import string
# import json
import logging


# try:
#     input = raw_input
# except NameError:
#     pass

# languages = {
#     'de': ['de-DE', 'KatjaNeural'],
#     'en': ['en-US', 'AriaNeural'],
#     'es': ['es-ES', 'HelenaRUS'],
#     'fr': ['fr-FR', 'HortenseRUS'],
#     'it': ['it-IT', 'ElsaNeural'],
#     'pt': ['pt-BR', 'FranciscaNeural']
# }

# __access_token__ = None
# __last_access__ = -1
# file_path = '.'


# def get_token():
#     fetch_token_url = "https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
#     headers = {
#         'Ocp-Apim-Subscription-Key': app.config['SPEECH_SUBCRIPTION_KEY']
#     }
#     response = requests.post(fetch_token_url, headers=headers)
#     global __access_token__
#     __access_token__ = str(response.text)
#     global __last_access__
#     __last_access__ = time.time()

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

        if 'SPEECH_ENDPOINT' not in app.config or \
                not app.config['SPEECH_ENDPOINT']:
            return '[ENDPOINT] Error: the translation service is not configured.'

        fetch_token_url = app.config['SPEECH_ENDPOINT']
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


def text_to_speech(text, lang):
    # key_name = 'SPEECH_SUBCRIPTION_KEY'
    # if not key_name in os.environ:
    #     raise Exception(
    #         'Please set/expot the enviroment variable: {}' .format(key_name))
    print(app.config)
    print()
    if 'SPEECH_SUBCRIPTION_KEY' not in app.config or \
            not app.config['SPEECH_SUBCRIPTION_KEY']:
        return '[KEY] Error: the translation service is not configured.'

    subscription_key = app.config['SPEECH_SUBCRIPTION_KEY']
    app = TextToSpeech(subscription_key, text, lang)
    app.get_token()
    app.save_audio()
    time = app.timestr
    return 'sample-' + time + '.wav'

    # t = time.time()
    # timestr = time.strftime("%Y%m%d_%H%M%S")+'_'+str(int(t) % 10000)
    # language = languages[lang][0]
    # name = languages[lang][1]

    # # TODO: Critical section
    # # Access Token is valid for 10 minutes
    # global __last_access__
    # if __last_access__ is -1 or t - __last_access__ >= 9*60:
    #     get_token()

    # # base_url = 'https://francecentral.tts.speech.microsoft.com/'
    # # path = 'cognitiveservices/v1'
    # constructed_url = 'https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1'
    # headers = {
    #     'Authorization': 'Bearer ' + __access_token__,
    #     'Content-Type': 'application/ssml+xml',
    #     'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
    #     'User-Agent': 'TMI-speech'
    # }
    # xml_body = ElementTree.Element('speak', version='1.0')
    # xml_body.set(
    #     '{http://www.w3.org/XML/1998/namespace}lang', language)
    # voice = ElementTree.SubElement(xml_body, 'voice')
    # voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
    # voice.set(
    #     'name', 'Microsoft Server Speech Text to Speech Voice (' + language + ', ' + name + ')')
    # voice.text = text
    # body = ElementTree.tostring(xml_body)

    # response = requests.post(constructed_url, headers=headers, data=body)
    # if response.status_code == 200:
    #     audio_path = file_path + 'sample-' + timestr + '.wav'
    #     with open(audio_path, 'wb') as audio:
    #         audio.write(response.content)
    #         logging.info("\nStatus code: " + str(response.status_code) +
    #                      "\nYour TTS is ready for playback.\n")
    #     return audio_path

    # else:
    #     logging.error("\nStatus code: " + str(response.status_code) +
    #                   "\nSomething went wrong. Check your subscription key and headers.\n")

    ######################
    ######################
    # timestr = time.strftime("%Y%m%d_%H%M%S")
    # language = languages[lang][0]
    # name = languages[lang][1]

    # endpoint_var = 'SPEECH_ENDPOINT'
    # if not endpoint_var in os.environ:
    #     raise Exception(
    #         'Please set/expot the enviroment variable: {}' .format(endpoint_var))
    # fetch_token_url = app.config[endpoint_var]
    # headers = {
    #     'Ocp-Apim-Subscription-Key': app.config['SPEECH_SUBCRIPTION_KEY']
    # }
    # response = requests.post(fetch_token_url, headers=headers)
    # access_token = str(response.text)

    # base_url = 'https://eastus.tts.speech.microsoft.com/'
    # path = 'cognitiveservices/v1'
    # constructed_url = base_url + path
    # headers = {
    #     'Authorization': 'Bearer ' + access_token,
    #     'Content-Type': 'application/ssml+xml',
    #     'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
    #     'User-Agent': 'TMI-speech'
    # }
    # xml_body = ElementTree.Element('speak', version='1.0')
    # xml_body.set(
    #     '{http://www.w3.org/XML/1998/namespace}lang', language)
    # voice = ElementTree.SubElement(xml_body, 'voice')
    # voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
    # voice.set(
    #     'name', 'Microsoft Server Speech Text to Speech Voice (' + language + ', ' + name + ')')
    # voice.text = text
    # body = ElementTree.tostring(xml_body)

    # response = requests.post(constructed_url, headers=headers, data=body)
    # if response.status_code == 200:
    #     audio_path = file_path + 'sample-' + timestr + '.wav'
    #     with open(audio_path, 'wb') as audio:
    #         audio.write(response.content)
    #         logging.info(
    #             f"\nStatus code: {response.status_code} \nYour TTS is ready for playback.\n")
    #     return audio_path

    # else:
    #     logging.error(
    #         f"\nStatus code: {response.status_code} \nSomething went wrong. Check your subscription key and headers.\n")
