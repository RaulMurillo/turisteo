from telegram import ReplyKeyboardMarkup, ParseMode, ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          MessageHandler, Filters, ConversationHandler)

from config import CONFIG
import texts
import util
import logging

logger = logging.getLogger(__name__)

# State definitions for Telegram Bot
(SELECTING_LANG, SELECTING_AUDIO, SELECTING_PICT, DISPLAY_INFO) = map(chr, range(4))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(START_OVER, LANG, AUDIO, PHOTO) = map(chr, range(10, 15))

# List of ingredients available in the system
# with open((COMMON_DIR / 'ingredients_es.csv'), 'r') as f:
#     INGREDIENTS = list(csv.reader(f))[0]

# Pictures folder
# PHOTO_DIR.mkdir(parents=True, exist_ok=True)


def start(update, context):
    """Select an action: query by recipes/ingredients or add preferences."""

    text = 'Puedo ayudarte a proponerte una receta con los ingredientes que me mandes en una imagen.\n' + \
        'Tambien puedes indicar tus preferencias y alergias.\n' + \
        'Selecciona la opción de que desees y pulsa <code>/exit</code> cuando hayas terminado\n\n'

    buttons = [['Quiero cocinar algo, pero no se me ocurre nada', 'Quiero preparar una receta concreta'],
               ['Añadir preferencia', 'Añadir alergia'],
               ['/exit']]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    # If we're starting over we don't need do send a new message
    if not context.user_data.get(START_OVER):
        update.message.reply_text(
            'Hola! Me llamo DASI-Chef Bot pero puedes llamarme Chef Bot.')
    update.message.reply_text(
        text=text, parse_mode=ParseMode.HTML, )  # resize_keyboard=True, reply_markup=keyboard)

    # Clear user context
    context.user_data.clear()
    context.user_data[START_OVER] = True
    return select_lang(update, context)

# TODO


def help(update, context):
    """Show software user manual in GUI"""

    text = 'Información actualmente no disponible :('
    update.message.reply_text(text=text)
    # return SELECTING_ACTION


def done(update, context):
    """Closes user conversation."""

    update.message.reply_text('Hasta la próxima!')

    context.user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""

    logger.error('Update "%s" caused error "%s"', update, context.error)

# https://github.com/dizballanze/m00dbot/blob/master/bot.py


def select_lang(update, context):
    # Select language
    button_list = [
        InlineKeyboardButton('{} {}'.format(texts.LANGUAGE[l]['name'], util.flag(texts.LANGUAGE[l]['flag'])), callback_data=l) for l in texts.LANGUAGE
    ]
    langs_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=4))

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
    langs_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=4))

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

    selection = '{} {}'.format(texts.YES_NO[context.user_data[LANG]]
                               [query.data], u'\U0001F50A' if query.data == 'yes' else u'\U0001F507')
    query.edit_message_text(
        text="{}\n{}".format(query.message.text, selection)
    )
    context.user_data[AUDIO] = query.data

    return select_pict(update, context)


def select_pict(update, context):
    query = update.callback_query
    query.answer()

    query.bot.send_message(
        chat_id=query.message.chat_id,
        text=texts.INSERT_PICT[context.user_data[LANG]],
        reply_markup=langs_markup,
        resize_keyboard=True,
    )

    return SELECTING_PICT


def process_pict(update, context):
    pass


def display_info(update, context):
    pass


def telegramBot_main(token):
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
            SELECTING_PICT: [MessageHandler(Filters.photo, process_pict), ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('help', help),
            CommandHandler('exit', done),
        ]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    telegramBot_main(CONFIG['telegram_token'])
