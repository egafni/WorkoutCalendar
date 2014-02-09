from wtforms_alchemy import ModelForm
from .. import WorkoutSession


class WorkoutSessionForm(ModelForm):
    class Meta:
        model = WorkoutSession
        field_args = {
        }

    exclude = ['created_on']