from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email


# ----------------------- Landing forms ----------------------- #
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
                                              message="Mex length is 50 char")])
    password = PasswordField(label="Password",
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired(message="Password is required"),
                                         Length(min=8, max=24,
                                                message="Password must be 8 - 24 char")])
    password2 = PasswordField(label="Re-type Password",
                              render_kw={"placeholder": "Re-type password"},
                              validators=[DataRequired(message="Password is required"),
                                          Length(min=8, max=24,
                                                 message="Password must be 8 - 24 char")])
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    """
    Login form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Length(min=1, max=75,
                                          message="Email must not exceed 75 char")])
    password = PasswordField(label="Password",
                             render_kw={"placeholder": "Password"},
                             validators=[DataRequired(message="Password is required"),
                                         Length(min=8, max=24,
                                                message="Password must be 8 - 24 char")])
    submit = SubmitField(label="Login")


class EmailForm(FlaskForm):
    """
    Request reset password form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
                                   Length(min=1, max=75,
                                          message="Email must not exceed 75 char")])
    submit = SubmitField(label="Submit")


class ResetForm(FlaskForm):
    """
    Reset password form for landing page.
    """
    email = EmailField(label="Email",
                       render_kw={"placeholder": "Example@example.com", "autofocus": True},
                       validators=[DataRequired(message="Email is required"),
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
                                                 message="Password must be 8 - 24 char")])
    submit = SubmitField(label="Reset")


# ----------------------- API forms ----------------------- #
class SearchPUBGForm(FlaskForm):
    """
    Search form for pubg page.
    """
    name = StringField(label="Steam name",
                       render_kw={"placeholder": "e.g. hambinooo"},
                       validators=[DataRequired(message="Name is required"),
                                   Length(min=3, max=50,
                                          message="Name must be 3-50 char long")])
    perspective = SelectField(label="Perspective",
                              choices=[("-fpp", "First Person"), ("", "Third person")])
    game_mode = SelectField(label="Game mode",
                            choices=[("solo", "Solo"), ("duo", "Duo"), ("squad", "Squad")])
    submit = SubmitField(label="Search")


# ----------------------- Game forms ----------------------- #
class CountryForm(FlaskForm):
    """
    Select form for countries page.
    """
    select = SelectField(label="Larger or Smaller?",
                         choices=[(1, "Larger"), (0, "Smaller")])
    submit = SubmitField(label="Go!")


class WordleForm(FlaskForm):
    """
    Word guess form for wordle page.
    """
    guess = StringField(render_kw={"placeholder": "Guess a word", "autofocus": True},
                        validators=[DataRequired(message="Please make a guess!"),
                                    Length(min=5, max=5,
                                           message="5 letters only!")])
    submit = SubmitField(label="Guess!")


class NumbersForm(FlaskForm):
    """
    Submit form for numbers page.
    """
    submit = SubmitField(label="Stop")
