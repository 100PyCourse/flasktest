from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from flasktest.games.utils import Wordle


class WordleWordCheck:
    def __init__(self, allowed_words, message=None):
        self.allowed_words = allowed_words

        if not message:
            message = "Word not accepted!"
        self.message = message

    def __call__(self, form, field):
        if not field.data.lower() in self.allowed_words:
            raise ValidationError(self.message)


class CountryForm(FlaskForm):
    """
    Select form for countries page.
    """
    select = SelectField(label="Larger or Smaller?",
                         choices=[("Larger", "Larger"), ("Smaller", "Smaller")])
    submit = SubmitField(label="Go!")


class WordleForm(FlaskForm):
    """
    Word guess form for wordle page.
    """
    guess = StringField(render_kw={"placeholder": "Guess a word", "autofocus": True},
                        validators=[DataRequired(message="Please make a guess!"),
                                    Length(min=5, max=5,
                                           message="5 letters only!"),
                                    WordleWordCheck(
                                        message="Word not accepted!",
                                        allowed_words=Wordle.word_list)])
    submit = SubmitField(label="Guess!")


class NumbersForm(FlaskForm):
    """
    Submit form for numbers page.
    """
    submit = SubmitField(label="Stop")
