from flask import make_response, request, jsonify, abort, render_template, send_file, Blueprint, flash, redirect, url_for
import json
from ..db import get_session
from .. import WorkoutSession
from .forms import WorkoutSessionForm
import datetime

session = get_session()
bprint = Blueprint('workout_calendar', __name__, template_folder='templates', static_folder='static')


@bprint.route('/')
def index():
    return render_template('index.html')


@bprint.route('/events/')
def events():
    wsessions = session.query(WorkoutSession).all()

    data = [dict(title=s.title, start=s.start.strftime('%Y-%m-%d'), id=s.id) for s in wsessions]
    #raise
    return json.dumps(data)


@bprint.route('/workout_session/add/', methods=['POST', 'GET'])
def add_workout_session():
    if request.method == 'POST':
        form = WorkoutSessionForm(request.form)
        if form.validate():
            d = {field.label.text: field.data for field in form}
            s = WorkoutSession(**d)
            session.add(s)
            session.commit()
            flash('Added %s' % s)
            return redirect(url_for("workout_calendar.index"))

    else:
        start = request.args.get('start')
        if start:
            start = datetime.datetime.strptime(start, '%Y-%m-%d').date()

        form = WorkoutSessionForm(request.form, start=start)
        return render_template("add_workout_session.html", form=form)


@bprint.route('/workout_session/copy/')
def copy_workout_session():
    source = session.query(WorkoutSession).get(request.args.get('id'))
    start = datetime.datetime.strptime(request.args.get('new_start'), '%Y-%m-%d').date()
    new_s = WorkoutSession(start=start)
    for c in source.__table__.c:
        if c.name not in ['id', 'start']:
            setattr(new_s, c.name, getattr(source, c.name))

    session.add(new_s)
    session.commit()
    return redirect(url_for("workout_calendar.index"))


@bprint.route('/workout_session/edit/', methods=['POST', 'GET'])
def edit_workout_session():
    if request.method == 'POST':
        id = int(request.form['id'])
        s = session.query(WorkoutSession).get(id)
        if request.form.get('delete', False):
            session.delete(s)
            session.commit()
            flash('Deleted %s' % s)
        else:
            form = WorkoutSessionForm(request.form)
            if form.validate():
                for field in form:
                    setattr(s, field.label.text, field.data)
                session.commit()
                flash('Updated %s' % s)
        return redirect(url_for("workout_calendar.index"))
    else:
        id = int(request.args.get('id'))
        s = session.query(WorkoutSession).get(id)
        assert s is not None, 'workout session does not exists'
        form = WorkoutSessionForm(obj=s)
        return render_template("edit_workout_session.html", form=form, id=id)

