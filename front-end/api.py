import time
from flask import Flask, request, send_from_directory
from flask import jsonify
import shutil
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from app.detect import detect_landmarks
from app.plot_rectangle import plot_rectangle
from app.google_search import google_search, google_fast_search
from app.web_scrap import get_entry_text, get_text_maxChars
from app.translate import short_translate, translate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)



shutil.rmtree(app.instance_path, ignore_errors=True)
# create the folders for runtime files when setting up your app
os.makedirs(os.path.join(app.instance_path, 'images'), exist_ok=True)
os.makedirs(os.path.join(app.instance_path, 'audios'), exist_ok=True)


@app.route('/save', methods=['POST'])
def save_image():
    file = request.files['file']
    lang = request.form['language']

    file.save(os.path.join(app.instance_path, 'images', file.filename))
    #filename = detect(file.filename)
    app.logger.info('[DETECT FUNCTION]')
    # Detect landmark on image and search on Google
    full_img_name = os.path.join(app.instance_path, 'images', file.filename)
    landmarks = detect_landmarks(full_img_name)
    landmark = landmarks[0]['description']
    app.logger.info(f'[LANDMARK] {landmark}')
    url = google_fast_search(query=landmark)
    app.logger.info(f'[URL] {url}')

    if lang != 'en':    # Translate title
        r = translate(landmark, source_language='en', dest_language=lang, app=app)
        landmark = r[0]['translations'][0]['text']
    
    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    
    rect_image_path = os.path.basename(plot_rectangle(
        full_img_name, (p0['x'], p0['y']), (p1['x'], p1['y']), os.getcwd()))
    app.logger.info(f'[RECT IMG] {rect_image_path}')
    info_text = get_entry_text(url)

    if lang != 'en':
        trans_text = translate(
            info_text, source_language='en', dest_language=lang, app=app)
        info_text = trans_text[0]["translations"][0]['text']
        app.logger.info('[TRADUCCION DONE]')



    return jsonify({'text': info_text, 'title': landmark})


@app.route('/detect/<path:imagename>/<lang>')
def detect(imagename, lang):
    app.logger.info('[DETECT FUNCTION]')
    # Detect landmark on image and search on Google
    full_img_name = os.path.join(app.instance_path, 'images', imagename)
    landmarks = detect_landmarks(full_img_name)
    landmark = landmarks[0]['description']
    app.logger.info(f'[LANDMARK] {landmark}')
    url = google_fast_search(query=landmark)
    app.logger.info(f'[URL] {url}')

    if lang != 'en':    # Translate title
        r = translate(landmark, source_language='en', dest_language=lang, app=app)
        landmark = r[0]['translations'][0]['text']
    
    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    
    rect_image_path = os.path.basename(plot_rectangle(
        full_img_name, (p0['x'], p0['y']), (p1['x'], p1['y']), os.getcwd()))
    app.logger.info(f'[RECT IMG] {rect_image_path}')
    info_text = get_entry_text(url)

    if lang != 'en':
        trans_text = translate(
            info_text, source_language='en', dest_language=lang, app=app)
        info_text = trans_text[0]["translations"][0]['text']
        app.logger.info('[TRADUCCION DONE]')



    return jsonify({'text': info_text, 'title': landmark})

@app.route('/img_show/<filename>')
def img_show(filename):
    return send_from_directory(os.path.join(app.instance_path, 'images'),
                               filename, as_attachment=True)

