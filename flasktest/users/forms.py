from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flasktest.models import User

banned_username_words = ['root', 'admin', 'sys', 'administrator']
banned_username_chars = "^(?=.*[-+_!'@#$%^&*., ?])"


class UsernameCheck:
    def __init__(self, banned_words, banned_chars, message=None):
        self.banned_words = banned_words
        self.banned_chars = banned_chars

        if not message:
            message = "Please choose another username!"
        self.message = message

    def __call__(self, form, field):
        if field.data.lower() in (word.lower() for word in self.banned_words):
            raise ValidationError(self.message)
        if len([x for x in list(self.banned_chars) if x in field.data]):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    """
    Register form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Email(message="Invalid email"),
                                   Length(min=1, max=75, message="Email must not exceed 75 char")])
    username = StringField(label="Username",
                           render_kw={"placeholder": "Username"},
                           validators=[DataRequired(message="Username is required"),
                                       Length(min=1, max=50,
                                              message="Mex length is 50 char"),
                                       UsernameCheck(
                                           message="Username or special characters not allowed",
                                           banned_words=banned_username_words,
                                           banned_chars=banned_username_chars),
                                       ])
    password = PasswordField(label="Password",
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired(message="Password is required"),
                                         Length(min=8, max=24,
                                                message="Password must be 8 - 24 char")])
    password2 = PasswordField(label="Re-type Password",
                              render_kw={"placeholder": "Re-type password"},
                              validators=[DataRequired(message="Passwords must match"),
                                          Length(min=8, max=24,
                                                 message="Password must be 8 - 24 char"),
                                          EqualTo("password")])
    submit = SubmitField(label="Register")

    def validate_email(self, email):
        """"
        Checks to see if a user with this email already exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered")


class LoginForm(FlaskForm):
    """
    Login form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Email(message="Invalid email"),
                                   Length(min=1, max=75,
                                          message="Email must not exceed 75 char"), ])
    password = PasswordField(label="Password",
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired(message="Password is required"),
                                         Length(min=8, max=24,
                                                message="Password must be 8 - 24 char")])
    submit = SubmitField(label="Login")

    def validate_email(self, email):
        """"
        Checks to see if a user with this email exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email not in database")


class EmailForm(FlaskForm):
    """
    Request reset password form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Email(message="Invalid email"),
                                   Length(min=1, max=75,
                                          message="Email must not exceed 75 char")])
    submit = SubmitField(label="Submit")

    def validate_email(self, email):
        """"
        Checks to see if a user with this email exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email not in database")


class ResetForm(FlaskForm):
    """
    Reset password form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Email(message="Invalid email"),
                                   Length(min=1, max=75,
                                          message="Email must not exceed 75 char")])
    reset_code = StringField(label="Reset code",
                             render_kw={"placeholder": "123456"},
                             validators=[DataRequired(message="Reset code is required"),
                                         Length(min=1, max=6,
                                                message="Code is six digits long.")])
    password = PasswordField(label="Password", render_kw={"placeholder": "Password"},
                             validators=[DataRequired(message="Password is required"),
                                         Length(min=8, max=24,
                                                message="Password must be 8 - 24 char")])
    password2 = PasswordField(label="Password", render_kw={"placeholder": "Password"},
                              validators=[DataRequired(message="Password is required"),
                                          Length(min=8, max=24,
                                                 message="Password must be 8 - 24 char"),
                                          EqualTo("password")])
    submit = SubmitField(label="Reset")

    def validate_email(self, email):
        """"
        Checks to see if a user with this email exists.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email not in database")
