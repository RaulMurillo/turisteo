import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    TRANSLATOR_TEXT_SUBSCRIPTION_KEY = os.environ.get(
        'TRANSLATOR_TEXT_SUBSCRIPTION_KEY')
    TRANSLATOR_TEXT_ENDPOINT = os.environ.get('TRANSLATOR_TEXT_ENDPOINT')
    SPEECH_SUBCRIPTION_KEY = os.environ.get('SPEECH_SUBCRIPTION_KEY')
    SPEECH_ENDPOINT = os.environ.get('SPEECH_ENDPOINT')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
        'GOOGLE_APPLICATION_CREDENTIALS')
    POSTS_PER_PAGE = 25
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'ico', 'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
