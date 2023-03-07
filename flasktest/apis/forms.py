from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


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
