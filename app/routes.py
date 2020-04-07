from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ImageForm
# from app.models import User, Post
from app.email import send_password_reset_email
from app.detect import detect_landmarks
from app.plot_rectangle import plot_rectangle
from app.google_search import google_search, google_fast_search
from app.web_scrap import get_entry_text, get_text_maxChars
from app.translate import short_translate, translate
from app.speech import text_to_speech

import os

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
    print('[DETECT FUNCTION]')
    # Detect landmark on image and search on Google
    full_img_name = os.path.join(app.instance_path, 'images', imagename)
    landmarks = detect_landmarks(full_img_name)
    landmark = landmarks[0]['description']
    print('[LANDMARK]', landmark)
    url = google_fast_search(query=landmark)
    print('[URL]', url)

    if lang != 'en':    # Translate title
        r = translate(landmark, source_language='en', dest_language=lang)
        landmark = r[0]['translations'][0]['text']

    # Landmark picture with rectangle
    p0, _, p1, _ = landmarks[0]['bounding_poly']['vertices']
    rect_image_path = os.path.basename(plot_rectangle(
        full_img_name, (p0['x'], p0['y']), (p1['x'], p1['y'])))
    print('[RECT IMG]', rect_image_path)
    # Informative text
    info_text = get_entry_text(url)
    if len(info_text) < 500:
        info_text = get_text_maxChars(url, maxChars=5000)
    print('[INFO TEXT SCRAPPED]')
    # Translate text
    if lang != 'en':
        trans_text = translate(
            info_text, source_language='en', dest_language=lang)
        info_text = trans_text[0]["translations"][0]['text']
        print('[TRADUCCION DONE]')

    # Generate audio
    if speech:
        audio = text_to_speech(info_text, lang=lang)
        # audio = text_to_speech("Hola mundo!", lang=lang)

        # os.path.join(app.instance_path, 'audios', audio)
        flash(f'Audio is {audio}')
        print('[AUDIO]', audio)
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


@app.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))
