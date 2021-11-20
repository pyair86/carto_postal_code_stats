from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):

    email = StringField(
        "Email",
        validators=[
            validators.Length(min=7, max=50),
            validators.DataRequired(message="Please enter a valid email address"),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[validators.DataRequired(message="Please enter a password")],
    )
