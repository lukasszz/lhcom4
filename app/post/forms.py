from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = PageDownField('Share your experience in a few words', validators=[
        DataRequired(), Length(min=1)])
    category = SelectField(choices=[['qauntum', 'Quantum'], ['softdevel', 'SoftDevel']])
    submit = SubmitField('Submit')
