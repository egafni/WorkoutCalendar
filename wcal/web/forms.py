# from wtforms_alchemy import ModelForm
# from .. import Workout
#
#
# class EventForm(ModelForm):
#     class Meta:
#         model = Workout
#         field_args = {
#         }
#
#     exclude = ['created_on']

from wtforms import StringField, TextAreaField
from wtforms import validators
from wtforms import Form

# def get_time():
#     timenow = datetime.datetime.now().replace(second=0, microsecond=0).time()
#     return datetime.datetime.combine(dateutil.parser.parse(start), timenow)

class WorkoutForm(Form):
    start = StringField('start', validators=[validators.DataRequired()])
    name = StringField('name', validators=[validators.DataRequired()])
    text = TextAreaField('text')

class MovementForm(Form):
    name = StringField('name', validators=[validators.DataRequired()])
    tempo = StringField('tempo')
    description = TextAreaField('description')