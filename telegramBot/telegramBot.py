from telegram import ReplyKeyboardMarkup, ParseMode, ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          MessageHandler, Filters, ConversationHandler)

from apis.detect import detect_landmarks
from apis.plot_rectangle import plot_rectangle
from apis.google_search import google_search, google_fast_search
from apis.web_scrap import get_entry_text, get_text_maxChars
from apis.translate import short_translate, translate
from apis.speech import text_to_speech

# from multiprocessing import Process
from telegram.ext.dispatcher import run_async, sleep
import texts
import util
import datetime
import logging

logger = logging.getLogger(__name__)

# State definitions for Telegram Bot
(SELECTING_LANG, SELECTING_AUDIO, SELECTING_PICT, DISPLAY_INFO) = map(chr, range(4))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(START_OVER, LANG, AUDIO, PHOTO, LANDMARK, LAT, LNG) = map(chr, range(10, 17))

# Keyboard buttons
button_list = ['/start', '/settings', '/help', '/exit']
keyboard = ReplyKeyboardMarkup(util.build_menu(button_list, n_cols=1))

PHOTO_DIR = None


def start(update, context):
    """Displays welcome message."""
    # choose_lang = True

    # If we're starting over we don't need do send a new message
    if not context.user_data.get(START_OVER):
        user = update.message.from_user
        try:
            context.user_data[LANG] = user.language_code
            logger.info(
                f'User language: {texts.LANGUAGE[context.user_data[LANG]]["name"]}')
            # choose_lang = False
        except:
            # Default lang
            context.user_data[LANG] = 'en'

        update.message.reply_text(
            texts.WELCOME[context.user_data[LANG]] + ' \U0001F5FA', parse_mode=ParseMode.HTML)

    text = texts.COMMANDS[context.user_data[LANG]]

    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML,
        # resize_keyboard=True, reply_markup=keyboard
    )

    # Clear user context
    context.user_data.clear()
    context.user_data[START_OVER] = True
    return select_lang(update, context)


def info(update, context):
    """Show software user manual in GUI"""

    # text = 'Información actualmente no disponible :('
    context.bot.send_message(chat_id=update.effective_chat.id, text=texts.INFO[context.user_data[LANG]], parse_mode=ParseMode.HTML)
    # update.message.reply_text(texts.INFO[context.user_data[LANG]], parse_mode=ParseMode.HTML)
    # return SELECTING_ACTION
    return


def done(update, context):
    """Closes user conversation."""
    if update.message != None:
        update.message.reply_text(texts.BYE[context.user_data[LANG]])
    else:
        query = update.callback_query
        query.answer()
        query.bot.send_message(
            chat_id=query.message.chat_id,
            text=texts.BYE[context.user_data[LANG]],
        )

    context.user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""

    logger.error('Update "%s" caused error "%s"', update, context.error)


def select_lang(update, context):

    context.user_data.clear()
    # Select language # https://github.com/dizballanze/m00dbot/blob/master/bot.py
    button_list = [
        InlineKeyboardButton('{} {}'.format(texts.LANGUAGE[l]['name'], util.flag(texts.LANGUAGE[l]['flag'])), callback_data=l) for l in texts.LANGUAGE
    ]
    langs_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=3))

    update.message.reply_text(
        text='Choose your language / Elige tu idioma / Choisissez votre langue',
        reply_markup=langs_markup,
        resize_keyboard=True,
    )
    return SELECTING_LANG


def process_lang(update, context):
    query = update.callback_query
    query.answer()

    selection = '{} {}'.format(texts.LANGUAGE[query.data]['name'], util.flag(
        texts.LANGUAGE[query.data]['flag']))
    query.edit_message_text(
        text="{}\n{}".format(query.message.text, selection)
    )
    context.user_data[LANG] = query.data

    return select_audio(update, context)


def select_audio(update, context):
    query = update.callback_query
    query.answer()

    # Select audio
    button_list = [
        InlineKeyboardButton('{} {}'.format(
            texts.YES_NO[context.user_data[LANG]]['yes'], u'\U0001F50A'), callback_data='yes'),
        InlineKeyboardButton('{} {}'.format(
            texts.YES_NO[context.user_data[LANG]]['no'], u'\U0001F507'), callback_data='no'),
    ]
    langs_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))

    query.bot.send_message(
        chat_id=query.message.chat_id,
        text=texts.AUDIO_QUESTION[context.user_data[LANG]],
        reply_markup=langs_markup,
        resize_keyboard=True,
    )
    return SELECTING_AUDIO


def process_audio(update, context):
    query = update.callback_query
    query.answer()
    context.user_data[AUDIO] = (query.data == 'yes')

    selection = '{} {}'.format(texts.YES_NO[context.user_data[LANG]]
                               [query.data], u'\U0001F50A' if context.user_data[AUDIO] else u'\U0001F507')
    query.edit_message_text(
        text="{}\n{}".format(query.message.text, selection)
    )

    return select_pict(update, context)


def select_pict(update, context):
    query = update.callback_query
    query.answer()

    query.bot.send_message(
        chat_id=query.message.chat_id,
        text=texts.INSERT_PICT[context.user_data[LANG]],
        reply_markup=keyboard,
        resize_keyboard=True,
    )

    return SELECTING_PICT


def process_pict(update, context):
    """Processes the image to generate the information."""
    # update.message.reply_text(
    #         'Genial! Voy a ver qué puedo hacer con todos estos ingredientes...')

    photo_file = update.message.photo[-1].get_file()
    currentDT = datetime.datetime.now()

    photo_name = 'user_photo' + \
        currentDT.strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'

    photo_path = PHOTO_DIR / photo_name
    photo_file.download(photo_path)
    logger.info("Image updated at %s", photo_path)

    context.user_data[PHOTO] = photo_path

    return display_info(update, context)

@run_async
@util.send_action(ChatAction.TYPING)
def display_name(update, context):
    # Translate landmark name
    landmark = short_translate(
        context.user_data[LANDMARK], source_language='en', dest_language=context.user_data[LANG])
    # Display landmark name
    update.message.reply_text(
        text='<b><u>' + landmark + '</u></b>', parse_mode=ParseMode.HTML)
    
    # sleep(1)
    # Display landmark location
    update.message.reply_location(
        latitude=context.user_data[LAT], longitude=context.user_data[LNG])
    
    logger.info(f'[LANDMARK] {context.user_data[LANDMARK]}')
    logger.info(
        f'[Lat. Lng.] {context.user_data[LAT]}; {context.user_data[LNG]}')

@run_async
@util.send_action(ChatAction.UPLOAD_PHOTO)
def display_image(update, context, landmarks):
    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    rect_image_path = plot_rectangle(context.user_data[PHOTO], p0, p1)
    # sleep(1)
    update.message.reply_photo(photo=open(rect_image_path, 'rb'))
    logger.info(f'[RECT IMG] {rect_image_path}')

@util.send_action(ChatAction.TYPING)
def my_translate(update, context, text, lang):
    tr = translate(text, source_language='en', dest_language=lang)

    return [t for t in tr if not(t == '\n' or len(t) < 50)]

@run_async
@util.send_action(ChatAction.TYPING)
def display_text(update, context, trans_text):
    for t in trans_text:
        sleep(0.75)
        update.message.reply_text(t)

    return 0

@run_async
def generate_audio(update, context, trans_text):
    audio_file = text_to_speech(
        ''.join(trans_text), lang=context.user_data[LANG])
    return audio_file


@util.send_action(ChatAction.RECORD_AUDIO)
def display_audio(update, context, audio_promise):
    audio_file = audio_promise.result()
    logger.info(f'[AUDIO] {audio_file}')
    update.message.reply_voice(open(audio_file, 'rb'))


@util.send_action(ChatAction.TYPING)
def display_info(update, context):
    img_name = context.user_data[PHOTO]
    lang = context.user_data[LANG]
    speech = context.user_data[AUDIO]

    # Detect landmark on image
    try:
        landmarks = detect_landmarks(img_name)

        context.user_data[LANDMARK] = landmarks[0]['description']
        context.user_data[LAT] = landmarks[0]["locations"][0]["lat_lng"]["latitude"]
        context.user_data[LNG] = landmarks[0]["locations"][0]["lat_lng"]["longitude"]
        ######
        # p_name = Process(target=display_name, args=(update, context))
        # p_name.start()
        display_name(update, context)
        ######

        # Get URL
        try:
            url = google_fast_search(query=context.user_data[LANDMARK])
        except:
            url = google_search(query=context.user_data[LANDMARK], num_res=1)[0]
        logger.info(f'[URL] {url}')

        ######
        # p_image = Process(target=display_image, args=(update, context, landmarks))
        # p_image.start()
        display_image(update, context, landmarks)
        ######

        # Get informative text
        info_text = get_entry_text(url)
        if len(info_text) < 500:
            info_text = get_text_maxChars(url, maxChars=5000)
        # logger.info('[INFO TEXT SCRAPPED]')
        # Translate text
        sleep(0.2)
        trans_text = my_translate(update, context, info_text, lang)
        # print(trans_text)
        # translate(info_text, source_language='en', dest_language=lang)
        # logger.info('[TRADUCCION DONE]')

        ######
        # p_text = Process(target=display_text, args=(update, context, trans_text))
        # p_text.start()
        text_promise = display_text(update, context, trans_text)
        ######

        # Generate audio
        if speech:
            ######
            # p_audio = Process(target=display_audio, args=(update, context, trans_text))
            # p_audio.start()
            audio_promise = generate_audio(update, context, trans_text)
            text_promise.result()
            display_audio(update, context, audio_promise)
            ######
        else:
            text_promise.result()
    except AttributeError:
        update.message.reply_text(
            text=texts.NO_LANDMARK[context.user_data[LANG]] + u' \U0001F625')
    except:
        update.message.reply_text(
            text=texts.NO_INFO[context.user_data[LANG]] + u' \U0001F625')

        # ######
        # p_name.join()
        # p_image.join()
        # p_text.join()
        # p_audio.join()
        # ######

    # Ask to continue
    button_list = [
        InlineKeyboardButton('{} {}'.format(
            texts.YES_NO[context.user_data[LANG]]['yes'], u'\U0001F44D'), callback_data='yes'),
        InlineKeyboardButton('{} {}'.format(
            texts.YES_NO[context.user_data[LANG]]['no'], u'\U0001F44E'), callback_data='no'),
    ]
    langs_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))

    update.message.reply_text(
        text=texts.CONTINUE_QUESTION[context.user_data[LANG]],
        reply_markup=langs_markup,
        resize_keyboard=True,
    )
    return DISPLAY_INFO


def telegramBot_main(token, photo_dir):
    """Creates and launches the Telegram Bot."""

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_LANG: [CallbackQueryHandler(process_lang, pattern='(en|es|fr|it|pt|de)')],
            SELECTING_AUDIO: [CallbackQueryHandler(process_audio, pattern='(yes|no)')],
            SELECTING_PICT: [MessageHandler(Filters.photo, process_pict), ],
            DISPLAY_INFO: [CallbackQueryHandler(done, pattern='no'),
                           CallbackQueryHandler(select_pict, pattern='yes')],
        },
        fallbacks=[
            CommandHandler('settings', select_lang),
            CommandHandler('help', info),
            CommandHandler('exit', done),
        ]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Pictures folder
    global PHOTO_DIR
    PHOTO_DIR = photo_dir
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    from credentials import TELEGRAM_CONFIG as CONFIG
    import os

    logging.root.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # PHOTO_DIR = CONFIG['UPLOADS_DIR']
    CONFIG['UPLOADS_DIR'].mkdir(parents=True, exist_ok=True)
    CONFIG['AUDIOS_DIR'].mkdir(parents=True, exist_ok=True)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG['GOOGLE_APPLICATION_CREDENTIALS']
    telegramBot_main(token=CONFIG['TELEGRAM_TOKEN'],
                     photo_dir=CONFIG['UPLOADS_DIR'])
