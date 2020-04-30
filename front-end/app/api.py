
  
import time
from flask import Flask, request, send_from_directory
from flask import jsonify
import shutil
import os
from app import app
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from app.detect import detect_landmarks
from app.plot_rectangle import plot_rectangle
from app.google_search import google_search, google_fast_search
from app.web_scrap import get_entry_text, get_text_maxChars
from app.translate import short_translate, translate
from config import Config







@app.route('/detect', methods=['POST'])
def detect_image():
    file = request.files['file']

    #lang = request.form['language']
    file.save(os.path.join(app.instance_path, 'images', file.filename))
    #filename = detect(file.filename)
    app.logger.info('[DETECT FUNCTION]')
    # Detect landmark on image and search on Google
    full_img_name = os.path.join(app.instance_path, 'images', file.filename)
    landmarks, latitud, longitud = detect_landmarks(full_img_name)
    landmark = landmarks[0]['description']
    app.logger.info(f'[LANDMARK] {landmark}')
   

    # if lang != 'en':    # Translate title
    #     r = translate(landmark, source_language='en', dest_language=lang)
    #     landmark = r[0]['translations'][0]['text']
    
    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']

    rect_image_path = plot_rectangle(full_img_name, p0, p1)
    rect_image_path = os.path.basename(rect_image_path)    
    app.logger.info(f'[RECT IMG] {rect_image_path}')
    
    return jsonify({'image_rect': rect_image_path, 'landmark': landmark, 'latitud': latitud, 'longitud': longitud})

    
@app.route('/title/<landmark>/<lang>')
def get_title(landmark, lang):
    if lang != 'en':    # Translate title
        r = translate(landmark, source_language='en', dest_language=lang)
        landmark = r[0]['translations'][0]['text']

    return jsonify({'title': landmark})


# @app.route('/detect/<path:imagename>/<lang>')
# def detect(imagename, lang):
#     app.logger.info('[DETECT FUNCTION]')
#     # Detect landmark on image and search on Google
#     full_img_name = os.path.join(app.instance_path, 'images', imagename)
#     landmarks = detect_landmarks(full_img_name)
#     landmark = landmarks[0]['description']
#     app.logger.info(f'[LANDMARK] {landmark}')
   

#     if lang != 'en':    # Translate title
#         r = translate(landmark, source_language='en', dest_language=lang, app=app)
#         landmark = r[0]['translations'][0]['text']
    
#     # Landmark picture with rectangle
#     p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    
#     rect_image_path = os.path.basename(plot_rectangle(
#         full_img_name, (p0['x'], p0['y']), (p1['x'], p1['y']), os.getcwd()))
#     app.logger.info(f'[RECT IMG] {rect_image_path}')
    
#     return jsonify({'title': landmark, 'image_rect': rect_image_path})

@app.route('/text/<landmark>/<lang>')
def get_text(landmark, lang):
    url = google_fast_search(query=landmark)
    app.logger.info(f'[URL] {url}')
    info_text = get_entry_text(url)

    if lang != 'en':
            trans_text = translate(
                info_text, source_language='en', dest_language=lang)
            info_text = trans_text[0]["translations"][0]['text']
            app.logger.info('[TRADUCCION DONE]')


    return jsonify({'text': info_text})



@app.route('/img_show/<filename>')
def img_show(filename):
    return send_from_directory(os.path.join(app.instance_path, 'images'),
                               filename, as_attachment=True)





