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

from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class EventForm(Form):
    start = TextField('start', validators=[DataRequired()])
    name = TextField('name', validators=[DataRequired()])
    text = TextAreaField('text', validators=[DataRequired()])