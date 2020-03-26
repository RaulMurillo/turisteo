#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from image_detection.detect import detect_landmarks
from image_detection.plot_rectangle import plot_rectangle
from web_scrapping.google_search import (google_search, google_fast_search)
from web_scrapping.web_scrap import (get_entry_text, get_text_maxChars)
from translator.translator import translate

import logging


class Turisteo:
    def __init__(self, lang='en'):
        self.lang = lang
        self.img = None
        self.speech = False

    def set_lang(self, lang):
        """Set the language of the application.

        lang (str): Must be a valid language code.
        Valid languages are in https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support
        """
        # TODO: Check if is a valid language
        self.lang = lang

    def set_img(self, path):
        """Set the image to analize.

        path (str): Path to the image.
        """
        # TODO: Check if is a valid path
        self.img = path

    def get_info(self, draw_rectangle=False):
        landmarks = detect_landmarks(self.img)
        logging.info(landmarks)

        q = landmarks[0]['description']
        url = google_fast_search(query=q)

        if draw_rectangle:
            logging.info(landmarks[0]['bounding_poly']['vertices'])
            p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
            
            p0 = (p0['x'], p0['y'])
            p1 = (p1['x'], p1['y'])
            plot_rectangle(self.img, p0, p1)

        logging.info(url)
        info_text = get_entry_text(url)
        if len(info_text) < 500:
            info_text = get_text_maxChars(url, maxChars=5000)
        logging.info(info_text)

        if self.lang != 'en':
            trans_text = translate(info_text, lang=self.lang, orig='en')
            logging.info(trans_text)






if __name__ == "__main__":
    from credentials import export_credentials
    export_credentials()

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
        

    app = Turisteo()
    app.set_lang('es')
    app.set_img('src/image_detection/resources/img2.jpg')
    app.get_info(draw_rectangle=True)
