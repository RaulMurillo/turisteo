from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import ImageForm
# from app.email import send_password_reset_email
from app.detect import detect_landmarks
from app.plot_rectangle import plot_rectangle
from app.google_search import google_search, google_fast_search
from app.web_scrap import get_entry_text, get_text_maxChars
from app.translate import short_translate, translate
from app.speech import text_to_speech

import os
import logging

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        image = form.image.data
        image.save(os.path.join(app.instance_path, 'images', image.filename))
        flash(f'Your image was uploaded! ({image.filename})')
        lang = form.language.data
        s = form.sound.data
        return redirect(url_for('detect', imagename=image.filename, lang=lang, speech=s))
    page = request.args.get('page', 1, type=int)
    posts = [None]
    next_url = None
    prev_url = None
    return render_template('index.html', title='Home', form=form,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/detect/<path:imagename>/<lang>/<int:speech>')
def detect(imagename, lang, speech):
    app.logger.info('[DETECT FUNCTION]')
    # Detect landmark on image and search on Google
    full_img_name = os.path.join(app.instance_path, 'images', imagename)
    landmarks = detect_landmarks(full_img_name)
    landmark = landmarks[0]['description']
    app.logger.info(f'[LANDMARK] {landmark}')
    app.logger.info(f'[GCP API RESPONSE]\n{landmarks}')
    url = google_fast_search(query=landmark)
    app.logger.info(f'[URL] {url}')

    if lang != 'en':    # Translate title
        r = translate(landmark, source_language='en', dest_language=lang)
        landmark = r[0]['translations'][0]['text']

    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    print(p0, p1)
    # print((p0['x'], p0['y']), (p1['x'], p1['y']))

    rect_image_path = os.path.basename(plot_rectangle(
        full_img_name, p0, p1)) #(p0['x'], p0['y']), (p1['x'], p1['y'])
    app.logger.info(f'[RECT IMG] {rect_image_path}')
    # Informative text
    info_text = get_entry_text(url)
    if len(info_text) < 500:
        info_text = get_text_maxChars(url, maxChars=5000)
    app.logger.info('[INFO TEXT SCRAPPED]')
    # Translate text
    if lang != 'en':
        trans_text = translate(
            info_text, source_language='en', dest_language=lang)
        info_text = trans_text[0]["translations"][0]['text']
        app.logger.info('[TRADUCCION DONE]')

    # Generate audio
    if speech:
        audio = text_to_speech(info_text, lang=lang)
        # audio = text_to_speech("Hola mundo!", lang=lang)

        # os.path.join(app.instance_path, 'audios', audio)
        flash(f'Audio is {audio}')
        app.logger.info(f'[AUDIO] {audio}')
    else:
        audio = None

    return render_template('detect.html', title='Image Detection',
                           landmark=landmark, image_path=rect_image_path,
                           info_text=info_text, speech=audio)


@app.route('/img_show/<filename>')
def img_show(filename):
    return send_from_directory(os.path.join(app.instance_path, 'images'),
                               filename, as_attachment=True)


@app.route('/audio_show/<filename>')
def audio_show(filename):
    print(filename)
    return send_from_directory(os.path.join(app.instance_path, 'audios'),
                               filename, as_attachment=True)

                            
@app.route('/translate', methods=['POST'])
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language']
                                      )[0]["translations"][0]['text']})

@app.route('/speech', methods=['POST'])
def speech_from_text():
    return jsonify({'audio': text_to_speech(request.form['text'],
                                            lang=request.form['language'])})
