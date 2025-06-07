from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField('Share your experience in a few words', validators=[
        DataRequired(), Length(min=1)])
    category = SelectField(choices=[['quantum', 'Quantum'], ['softdevel', 'SoftDevel']])
    header_image = FileField('Header Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Submit')
