from flask.ext.admin.contrib import sqla
from flask.ext.admin import Admin, BaseView, expose

from ..app import flask_app, db
from ..models import Movement, Workout, Work


class MovementAdmin(sqla.ModelView):
    pass
    # column_display_pk = True
    # form_columns = ['id', 'desc']


class WorkoutAdmin(sqla.ModelView):
    form_widget_args = {
        'notes': {
            'class_': 'ckeditor'
        }
    }
    inline_models = (Work,)
    # column_display_pk = True
    form_columns = ['start', 'name', 'notes', 'work']


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


# Create admin
admin = Admin(flask_app, name='Workout Calendar')
admin.add_view(MovementAdmin(Movement, db.session))
admin.add_view(WorkoutAdmin(Workout, db.session))
#admin.add_view(MyView(name='Home'))