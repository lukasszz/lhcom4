from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField('Share your experience in a few words', validators=[
        DataRequired(), Length(min=1)])
    category = SelectField(choices=[['quantum', 'Quantum'], ['softdevel', 'SoftDevel']])
    timestamp = DateTimeLocalField('Timestamp', format='%Y-%m-%dT%H:%M')
    header_image = FileField('Header Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    content_images = FileField('Content Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ], render_kw={'multiple': True})
    submit = SubmitField('Submit')
