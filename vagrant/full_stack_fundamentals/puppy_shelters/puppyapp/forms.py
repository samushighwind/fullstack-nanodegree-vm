from flask.ext.wtf import Form
from wtforms.fields import (
    StringField, SelectField, RadioField,
    TextAreaField, IntegerField, SelectMultipleField
)
from wtforms.fields.html5 import DateField, URLField, DecimalField
from wtforms.validators import DataRequired, Optional, AnyOf, NumberRange, URL
from wtforms.widgets import ListWidget, CheckboxInput
import datetime


class PuppyProfileForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        choices=[("female", "female"), ("male", "male")],
        validators=[DataRequired()]
    )
    birthdate = DateField(
        "Birthdate",
        validators=[DataRequired()],
        default=datetime.date.today()
    )
    weight = DecimalField(
        "Weight (lbs.)",
        validators=[DataRequired(), NumberRange(min=1.0, max=40.0)]
    )
    picture = URLField("Photo URL", validators=[Optional(), URL()])
    description = TextAreaField("Description")
    special_needs = TextAreaField("Special Needs")


class AdopterProfileForm(Form):
    name = StringField("Name", validators=[DataRequired()])


class ShelterProfileForm(Form):
    name = StringField("Name", validators=[DataRequired()])    
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("ZIP Code")
    website = URLField("Website", validators=[Optional(), URL()])
    maximum_capacity = IntegerField(
        "Maximum Capacity",
        validators=[DataRequired(), NumberRange(min=1, max=500)]
    )


class ShelterTransferForm(Form):
    # for a ShelterTransferForm, form, form.shelter_id.choices must be
    # dynamically set before use.
    shelter_id = RadioField(validators=[DataRequired()], coerce=int)


# override found at:
# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class PuppyAdoptionForm(Form):
    # for a PuppyAdoptionForm, form, form.adopter_ids.choices must be
    # dynamically set before use.
    adopter_ids = MultiCheckboxField(validators=[DataRequired()], coerce=int)