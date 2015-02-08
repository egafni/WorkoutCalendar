import json
import datetime

from flask import request, render_template, Blueprint, flash, redirect, url_for
import dateutil.parser

from ..models import Workout, Movement
from .forms import WorkoutForm, MovementForm
from ..app import session


bprint = Blueprint('wcal', __name__, template_folder='templates', static_folder='static')


@bprint.route('/')
def index():
    return render_template('index.html')


@bprint.route('/events/')
def events():
    workouts = session.query(Workout).all()

    data = [dict(title=workout.name, start=workout.start.isoformat(), id=workout.id) for workout in workouts]
    return json.dumps(data)


@bprint.route('/movement_index')
def movement_index():
    movements = session.query(Movement).all()
    return render_template('movement/index.html', movements=movements)


@bprint.route('/movement/add/', methods=['POST', 'GET'])
def movement_add():
    print request.environ['REQUEST_METHOD']
    return generic_add(MovementForm(request.form), Movement)


@bprint.route('/workout/add/', methods=['GET', 'POST'])
def workout_add():
    form = WorkoutForm(request.form)
    if request.method == 'GET':
        assert 'start' in request.args
        start = request.args.get('start')
        # add time to date
        timenow = datetime.datetime.now().replace(second=0, microsecond=0).time()
        start = datetime.datetime.combine(dateutil.parser.parse(start), timenow)
        form.start.data = start

    return generic_add(form, Workout)


def generic_add(form, Model):
    if request.method == 'POST' and form.validate():
        d = {field.label.text: field.data for field in form if field.label.text != 'Csrf Token'}
        s = Model(**d)
        session.add(s)
        session.commit()
        flash('Added %s' % s)
        return redirect(url_for("wcal.index"))
    else:
        return render_template("add.html", form=form)


@bprint.route('/workout/copy/<int:id>/')
@bprint.route('/workout/copy/')  # for fullcalendar endpoint
def workout_copy(id=None):
    if id is None:
        id = request.get['id']
    source_workout = session.query(Workout).get(id)
    new_workout = Workout(start=request.args.get('new_start'))
    for c in source_workout.__table__.c:
        if c.name not in ['id', 'start', 'created_on']:
            setattr(new_workout, c.name, getattr(source_workout, c.name))

    session.add(new_workout)
    session.commit()
    return redirect(url_for("wcal.index"))


@bprint.route('/workout/delete/<int:id>')
def workout_delete(id):
    workout = session.query(Workout).get(id)
    session.delete(workout)
    session.commit()
    flash('Deleted %s' % workout)
    return redirect(url_for("wcal.index"))


# EDIT
@bprint.route('/movement/<int:id>')
def movement(id):
    return edit(Movement, id)


@bprint.route('/workout/edit/<int:id>/', methods=['POST', 'GET'])
@bprint.route('/workout/edit/')  # for fullcalendar endpoint
def workout_edit(id=None):
    if id is None:
        id = request.get['id']
    return edit(Workout, id)


def edit(Model, id):
    workout = session.query(Model).get(id)
    form = WorkoutForm(request.form, obj=workout)
    if request.method == 'POST' and form.validate():
        for field in form:
            print 'SET %s %s'
            setattr(workout, field.label.text, field.data)
        session.commit()
        flash('Updated %s' % workout)
        return redirect(url_for("wcal.index"))
    else:
        return render_template("edit.html", form=form, id=id)