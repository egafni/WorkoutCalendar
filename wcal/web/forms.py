# from wtforms_alchemy import ModelForm
# from .. import Workout
#
#
# class EventForm(ModelForm):
# class Meta:
# model = Workout
# field_args = {
#         }
#
#     exclude = ['created_on']
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms import validators
from wtforms import Form

from ..app import db
from ..models import Movement



# def get_time():
#     timenow = datetime.datetime.now().replace(second=0, microsecond=0).time()
#     return datetime.datetime.combine(dateutil.parser.parse(start), timenow)

def WorkoutForm(*args, **kwargs):
    """
    Functor used to set exercise choices
    """

    class WorkoutForm(Form):
        start = StringField('start', validators=[validators.DataRequired()])
        name = StringField('name', validators=[validators.DataRequired()])
        movements = SelectMultipleField('movements')
        text = TextAreaField('text')

    form = WorkoutForm(*args, **kwargs)
    movements = db.session.query(Movement).all()
    form.movements.choices = [(str(m.id), m.name) for m in movements]
    return form


class MovementForm(Form):
    name = StringField('name', validators=[validators.DataRequired()])
    tempo = StringField('tempo')
    description = TextAreaField('description')

    # class WorkoutForm(ModelForm):
    #     class Meta:
    #         Model = Workout
    #
    # class MovementForm(ModelForm):
    #     class Meta:
    #         Model = Movement