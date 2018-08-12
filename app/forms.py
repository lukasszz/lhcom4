from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class JrnlForm(FlaskForm):
    jrnl = TextAreaField('Share your experience in a few words', validators=[
        DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')