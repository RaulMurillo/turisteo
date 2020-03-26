#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from image_detection.detect import detect_landmarks
from image_detection.plot_rectangle import plot_rectangle
from web_scrapping.google_search import (google_search, google_fast_search)
from web_scrapping.web_scrap import (get_entry_text, get_text_maxChars)
from translator.translator import translate
from speech.speech import TextToSpeech

import logging


class Turisteo:
    def __init__(self, translator_key, speech_key, lang='en', speech=False):
        self.translator_key = translator_key
        self.speech_key = speech_key
        self.lang = lang
        self.img = None
        self.speech = speech

    def set_lang(self, lang):
        """Set the language of the application.

        lang (str): Must be a valid language code.
        Valid languages are in https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support
        """
        # TODO: Check if is a valid language
        self.lang = lang

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

        if self.lang != 'en':
            trans_text = translate(info_text, lang=self.lang, orig='en')
            logging.debug(trans_text)
            assert self.lang == trans_text["translations"][0]['to']
            response['text'] = trans_text["translations"][0]['text']
        else:
            # trans_text = {"translations": [{"text": info_text, "to": "en"}]}
            response['text'] = info_text

        logging.info(response['text'])

        if self.speech:
            speechAPI = TextToSpeech(
                self.speech_key, response['text'], self.lang)
            speechAPI.get_token()
            audio = speechAPI.save_audio(file_path='src/resources/audios/')
            response['audio'] = audio

        return response


if __name__ == "__main__":
    from credentials import export_credentials
    trans_key, speech_key = export_credentials()

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)

    app = Turisteo(trans_key, speech_key, speech=True)
    app.set_lang('es')
    app.set_img('src/resources/images/test.jpg')
    print(app.get_info(draw_rectangle=True))
