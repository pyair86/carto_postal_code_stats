from wtforms import Form, validators, StringField, PasswordField
from wtforms.validators import Email


class RegistrationForm(Form):
    email = StringField(
        "Email Address",
        [validators.Length(min=6, max=50), validators.DataRequired(), Email()],
    )
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
            validators.Length(min=6, max=50),
        ],
    )
    confirm = PasswordField("Repeat Password")
