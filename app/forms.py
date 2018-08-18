from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class JrnlForm(FlaskForm):
    jrnl = TextAreaField('Share your experience in a few words', validators=[
        DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')