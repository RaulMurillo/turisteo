#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from image_detection.detect import detect_landmarks
from image_detection.plot_rectangle import plot_rectangle
from web_scrapping.google_search import (google_search, google_fast_search)
from web_scrapping.web_scrap import (get_entry_text, get_text_maxChars)
from translator.translator import TranslatorText
from speech.speech import TextToSpeech

import logging


class Turisteo:
    def __init__(self, lang='en', speech=False, img=None):
        self.lang = lang
        self.img = img
        self.bSpeech = speech
        self.api = {
            'translate': None,
            'speech': None
        }

    def init_translate(self, subscription_key):
        self.api['translate'] = TranslatorText(
            subscription_key, lang=self.lang, orig='en')

    def init_speech(self, subscription_key):
        self.api['speech'] = TextToSpeech(subscription_key, lang=self.lang)
        self.api['speech'].get_token()

    def set_lang(self, lang):
        """Set the language of the application.

        lang (str): Must be a valid language code.
        Valid languages are in https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support
        """
        # TODO: Check if is a valid language
        self.lang = lang
        if self.api['translate'] is not None:
            self.api['translate'].set_lang(lang, orig='en')
        if self.bSpeech and self.api['speech'] is not None:
            try:
                self.api['speech'].set_lang(lang)
            except ValueError:
                self.bSpeech = False

    def set_img(self, path):
        """Set the image to analize.

        Args:
            path (str): Path of the image.  
        """
        # TODO: Check if is a valid path
        self.img = path

    def get_info(self, draw_rectangle=False):
        """Get information from the image.

        Args:
            draw_rectangle (bool): If `True`, generates a rectangle around the monument in the image. Default is `False`.

        Returns:
            dict: Requested information. At least, `text` key is present. Optional `image` and `audio` keys indicate corresponding paths to image with rectangle and text-audio conversion, respectively.
        """
        landmarks = detect_landmarks(self.img)
        logging.info(landmarks)

        q = landmarks[0]['description']
        url = google_fast_search(query=q)

        response = {'text': ''}

        if draw_rectangle:
            logging.info(landmarks[0]['bounding_poly']['vertices'])
            p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']

            p0 = (p0['x'], p0['y'])
            p1 = (p1['x'], p1['y'])
            rect = plot_rectangle(self.img, p0, p1)
            response['image'] = rect

        logging.info(url)
        info_text = get_entry_text(url)
        if len(info_text) < 500:
            info_text = get_text_maxChars(url, maxChars=5000)
        logging.info(info_text)

        # Translate text
        if self.lang != 'en':
            # trans_text = translate(info_text, lang=self.lang, orig='en')
            # logging.debug(trans_text)
            # assert self.lang == trans_text["translations"][0]['to']
            # response['text'] = trans_text["translations"][0]['text']
            if self.api['translate'] is None:
                raise Exception('Uninitialized Translator Text API.')
            self.api['translate'].set_text(info_text)
            trans_text = self.api['translate'].translate()
            logging.debug(trans_text)
            response['text'] = trans_text["translations"][0]['text']
        else:
            # trans_text = {"translations": [{"text": info_text, "to": "en"}]}
            response['text'] = info_text

        logging.info(response['text'])

        # Generate audio
        if self.bSpeech:
            if self.api['speech'] is None:
                raise Exception('Uninitialized Text to Speech API.')
            self.api['speech'].set_text(response['text'])
            audio = self.api['speech'].save_audio(
                file_path='src/resources/audios/')
            response['audio'] = audio

        return response


if __name__ == "__main__":
    from credentials import export_credentials
    trans_key, speech_key = export_credentials()

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    app = Turisteo(speech=True)
    app.init_translate(trans_key)
    app.init_speech(speech_key)
    app.set_lang('pt')
    app.set_img('src/resources/images/test.jpg')
    print(app.get_info(draw_rectangle=True))
