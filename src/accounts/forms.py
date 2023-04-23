from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, IntegerField, PasswordField,
                     SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.accounts.models import User
from src.organisations.models import Organisation


class SetAdminForm(FlaskForm):
    user_id = IntegerField("User id", validators=[DataRequired()])
    is_admin = BooleanField("Admin")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    organisation = SelectField("Organisation", choices=[(
        o.id, o.name) for o in Organisation.query.order_by('name').all()], validators=[DataRequired()])
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
