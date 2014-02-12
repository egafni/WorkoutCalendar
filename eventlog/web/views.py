from flask import make_response, request, jsonify, abort, render_template, send_file, Blueprint, flash, redirect, url_for
import json
from .. import Event
from .forms import EventForm
import datetime
import dateutil.parser


def gen_bprint(session):
    bprint = Blueprint('workout_calendar', __name__, template_folder='templates', static_folder='static')


    @bprint.route('/')
    def index():
        return render_template('index.html')


    @bprint.route('/events/')
    def events():
        events = session.query(Event).all()

        data = [dict(title=event.name, start=event.start.isoformat(), id=event.id) for event in events]
        return json.dumps(data)


    @bprint.route('/event/add/', methods=['POST', 'GET'])
    def event_add():
        form = EventForm(request.form)
        if request.method == 'POST' and form.validate():
            d = {field.label.text: field.data for field in form if field.label.text != 'Csrf Token'}
            s = Event(**d)
            session.add(s)
            session.commit()
            flash('Added %s' % s)
            return redirect(url_for("workout_calendar.index"))
        else:
            if request.form.get('start') is None:
                start = request.args.get('start')
                timenow = datetime.datetime.now().replace(second=0, microsecond=0).time()
                start = datetime.datetime.combine(dateutil.parser.parse(start), timenow)
                #start = dateutil.parser.parse(start)
                form.start.data = start
            return render_template("event_add.html", form=form)


    @bprint.route('/event/copy/')
    def event_copy():
        source_event = session.query(Event).get(request.args.get('id'))
        new_event = Event(start=dateutil.parser.parse(request.args.get('new_start')))
        for c in source_event.__table__.c:
            if c.name not in ['id', 'start', 'created_on']:
                setattr(new_event, c.name, getattr(source_event, c.name))

        session.add(new_event)
        session.commit()
        return redirect(url_for("workout_calendar.index"))


    @bprint.route('/event/delete/')
    def event_delete():
        id = int(request.args['id'])
        event = session.query(Event).get(id)
        session.delete(event)
        session.commit()
        flash('Deleted %s' % event)
        return redirect(url_for("workout_calendar.index"))

    @bprint.route('/event/edit/', methods=['POST', 'GET'])
    def event_edit():
        id = int(request.args['id'])
        event = session.query(Event).get(id)
        form = EventForm(request.form, obj=event)
        if request.method == 'POST' and form.validate():
            for field in form:
                setattr(event, field.label.text, field.data)
            session.commit()
            flash('Updated %s' % event)
            return redirect(url_for("workout_calendar.index"))
        else:
            return render_template("event_edit.html", form=form, id=id)

    return bprint