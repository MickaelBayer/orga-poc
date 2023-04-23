from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.accounts.models import User
from src.organisations.models import Organisation


class CreateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description (optional)")
