from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    url = StringField('enter URL', validators=[
        DataRequired(),
        URL(require_tld=True, message="invalid URL")
    ])
    submit = SubmitField('add')