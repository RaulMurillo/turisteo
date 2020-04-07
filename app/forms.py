from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, FileField, RadioField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, regexp
from app import app
import re


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # def validate_username(self, username):
    #     if username.data != self.original_username:
    #         user = User.query.filter_by(username=self.username.data).first()
    #         if user is not None:
    #             raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ImageForm(FlaskForm):
    # post = TextAreaField('Say something', validators=[DataRequired()])
    # image = FileField('Image File', validators=[regexp(r'^[^/\\]\.jpg$')])
    image = FileField('Image File', validators=[DataRequired()])
    language = SelectField('Language', choices=[
        ('en', '\U0001F1FA\U0001F1F8 English (US)'),
        ('es', '\U0001F1EA\U0001F1F8 Spanish'),
        ('fr', '\U0001F1EB\U0001F1F7 French'),
        ('de', '\U0001F1E9\U0001F1EA German'),
        ('it', '\U0001F1EE\U0001F1F9 Italian'),
        ('pt', '\U0001F1E7\U0001F1F7 Portuguese (Brazil audio)'),
        ('zh-Hans', '\U0001F1E8\U0001F1F3 Chinese (Simplified)')
    ], validators=[DataRequired()])
    sound = BooleanField('Sound')
    submit = SubmitField('Submit')

    def validate_image(self, image):
        filename = image.data.filename
        if filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
            raise ValidationError(
                'Unsupported file extension. Please use a different file.')

        image.data.filename = re.sub(r'[^a-z0-9_.-]', '_', filename)
