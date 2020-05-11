import os
import requests
import time
from xml.etree import ElementTree
import logging
from credentials import TELEGRAM_CONFIG as CONFIG

# __subscription_key__ = None
# __access_token__ = None
languages = {
    'de': ['de-DE', 'KatjaNeural'],
    'en': ['en-US', 'AriaNeural'],
    'es': ['es-ES', 'HelenaRUS'],
    'fr': ['fr-FR', 'HortenseRUS'],
    'it': ['it-IT', 'ElsaNeural'],
    'pt': ['pt-BR', 'FranciscaNeural']
}
file_path = './'


def get_token():
    if 'SPEECH_SUBCRIPTION_KEY' not in CONFIG or \
            not CONFIG['SPEECH_SUBCRIPTION_KEY']:
        return 'Error: the translation service is not configured.'

    # TODO: Change Azure region (eastus->francecentral)
    fetch_token_url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken' #'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    headers = {
        'Ocp-Apim-Subscription-Key': CONFIG['SPEECH_SUBCRIPTION_KEY']
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token


def text_to_speech(text, lang):
    timestr = time.strftime("%Y%m%d_%H%M")
    try:
        language = languages[lang][0]
        name = languages[lang][1]
    except KeyError:
        logging.error('Unsupported language for text_to_speech function.')
        return None

    # Get token
    t = time.time()
    # TODO: Token is valid for 10 minutes.
    # Improve efficiency by reducing API calls
    access_token = get_token()

    # Save audio
    constructed_url = 'https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1' #'https://eastus.tts.speech.microsoft.com/cognitiveservices/v1'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3',#'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'TMI-speech'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set(
        '{http://www.w3.org/XML/1998/namespace}lang', language)
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
    voice.set(
        'name', 'Microsoft Server Speech Text to Speech Voice (' + language + ', ' + name + ')')
    voice.text = text
    body = ElementTree.tostring(xml_body)

    response = requests.post(constructed_url, headers=headers, data=body)
    if response.status_code == 200:
        audio_file = 'sample_' + timestr + str(int(t*100) % 10000) + '.mp3'#.wav'
        with open((CONFIG['AUDIOS_DIR'] / audio_file), 'wb') as audio:
            audio.write(response.content)
            logging.info("\nStatus code: " + str(response.status_code) +
                         "\nYour TTS is ready for playback.\n")
        return (CONFIG['AUDIOS_DIR'] / audio_file)

    else:
        logging.error("\nStatus code: " + str(response.status_code) +
                      "\nSomething went wrong. Check your subscription key and headers.\n")

    return None
