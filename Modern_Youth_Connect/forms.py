from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Modern_Youth_Connect.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    SSC_marks = StringField('SSC Marks', validators=[DataRequired(), Length(min=2, max=20)])
    SSC_marksheet = FileField('Upload Marksheet', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    HSC_marks = StringField('HSC Marks', validators=[DataRequired(), Length(min=2, max=20)])
    HSC_marksheet = FileField('Upload Marksheet', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    BSC_marks = StringField('BSc Marks', validators=[DataRequired(), Length(min=2, max=20)])
    BSC_marksheet = FileField('Upload Marksheet', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    MSC_marks = StringField('MCS marks', validators=[DataRequired(), Length(min=2, max=20)])
    MSC_marksheet = FileField('Upload Marksheet', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        new_user = User.query.filter_by(username=username.data).one_or_none()
        if new_user:
            raise ValidationError('This username is already taken')

    def validate_email(self, email):
        new_user = User.query.filter_by(email=email.data).one_or_none()
        if new_user:
            raise ValidationError('User with this email already exists')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    def validate_username(self, username):
        """
        User may leave blank field also and try to update for that we need to validate it first and also check if it is already taken
        :param username:
        :return: Validation Error if true
        """
        if username.data != current_user.username:
            new_user = User.query.filter_by(username=username.data).first()
            if new_user:
                raise ValidationError('this username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            new_user = User.query.filter_by(email=email.data).first()
            if new_user:
                raise ValidationError('this email is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
