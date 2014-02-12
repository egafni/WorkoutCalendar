# from wtforms_alchemy import ModelForm
# from .. import Event
#
#
# class EventForm(ModelForm):
#     class Meta:
#         model = Event
#         field_args = {
#         }
#
#     exclude = ['created_on']

from wtforms import TextField, TextAreaField
from wtforms import validators
from wtforms import Form

class EventForm(Form):
    start = TextField('start', validators=[validators.Required()])
    name = TextField('name', validators=[validators.Required()])
    text = TextAreaField('text', validators=[validators.Required()])