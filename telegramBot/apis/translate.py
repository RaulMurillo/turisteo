import json
import requests
#from app import app
import uuid
import logging
from credentials import TELEGRAM_CONFIG as CONFIG

# __subscription_key__ = None
# __endpoint__ = 'https://api.cognitive.microsofttranslator.com'


# def init_ms_translate_api():
#     global __subscription_key__
#     # global __endpoint__
#     key_var = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
#     if key_var not in app.config or \
#             not app.config[key_var]:
#         raise Exception(
#             'Please set/expot the enviroment variable: {}' .format(key_var))
#     subscription_key = app.config[key_var]

# endpoint_var = 'TRANSLATOR_TEXT_ENDPOINT'
# if endpoint_var not in app.config or \
#         not app.config[endpoint_var]:
#     raise Exception(
#         'Please set/export the environment variable: {}'.format(endpoint_var))
# endpoint = app.config[endpoint_var]


MAX_LENGTH = 2500


def split(text):
    """ Split a long text on paragraphs, or lines if needed. """
    paragraphs = text.splitlines(keepends=True)
    for i, p in enumerate(paragraphs):
        if len(p) > MAX_LENGTH:
            # Split in sentences
            lines = p.split('. ')
            lines = [l + '. ' for l in lines]
            paragraphs = paragraphs[:i] + lines + paragraphs[i+1:]
    return paragraphs


def short_translate(text, source_language, dest_language):
    if dest_language == source_language:
        return text
    
    if 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY' not in CONFIG or \
            not CONFIG['TRANSLATOR_TEXT_SUBSCRIPTION_KEY']:
        return 'Error: the translation service is not configured.'

    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}'.format(
        source_language, dest_language)

    headers = {
        'Ocp-Apim-Subscription-Key': CONFIG['TRANSLATOR_TEXT_SUBSCRIPTION_KEY'],
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    r = requests.post(url, headers=headers, json=[{"text": text}])
    if r.status_code != 200:
        return 'Error: the translation service failed.'
    return json.loads(r.content.decode('utf-8-sig'))[0]['translations'][0]['text']


def translate(text, source_language, dest_language):
    if 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY' not in CONFIG or \
            not CONFIG['TRANSLATOR_TEXT_SUBSCRIPTION_KEY']:
        return 'Error: the translation service is not configured.'
    if len(text) > MAX_LENGTH:
        trad_in = split(text)
    else:
        trad_in = [text]

    if dest_language == source_language:
        return trad_in

    url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}'.format(
        source_language, dest_language)

    headers = {
        'Ocp-Apim-Subscription-Key': CONFIG['TRANSLATOR_TEXT_SUBSCRIPTION_KEY'],
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    response = [requests.post(url, headers=headers, json=[
        {"text": text}]).json()[0] for text in trad_in]

    # r = requests.post(url, headers=headers, json=[{"text": text}])
    # if r[0].status_code != 200:
    #     return 'Error: the translation service failed.'
    
    # # Merge translated pieces of text
    # for r in response[1:]:
    #     response[0]['translations'][0]['text'] += r['translations'][0]['text']
    logging.debug(response)
    # return response[:1]
    return [r['translations'][0]['text'] for r in response]
