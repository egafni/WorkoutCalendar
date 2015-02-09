import os
import datetime

from flask import url_for
from sqlalchemy import Column, Integer, String, DateTime, func, Text, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
import dateutil.parser

from .app import db


opj = os.path.join

# movements_2_workout = db.Table('movements_2_workout',
#                                db.Column('movement_id', db.Integer, db.ForeignKey('movement.id')),
#                                db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'))
# )

class Work(db.Model):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    left_id = Column(Integer, ForeignKey('movement.id'))
    right_id = Column(Integer, ForeignKey('workout.id'))
    movement = db.relationship("Movement", backref="work_assocs")
    tempo = Column(String(50))
    amount = Column(db.String)


class Workout(db.Model):
    __tablename__ = 'workout'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    _start = Column('start', DateTime, nullable=False)
    # date = Column(Date, nullable=False)
    # end = Column(DateTime, nullable=True)
    # time = Column(Time)
    # date_end = Column(Date)
    # time_end = Column(Time)
    name = Column(String, nullable=False)
    notes = Column(Text)
    work = db.relationship('Work', backref="workout")

    def __init__(self, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)

    @hybrid_property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        self._start = dateutil.parser.parse(val) if isinstance(val, str) or isinstance(val, unicode) else val

    def date_isoformat(self):
        if self.time is None:
            return self.date.isoformat()
        else:
            return datetime.datetime.combine(self.date, self.time).isoformat()

    def __repr__(self):
        return '<Workout "{0}" [{1}]>'.format(self.name, self.start.strftime('%Y-%m-%d') if self.start else '')

    @property
    def url(self):
        return url_for('wcal.workout', id=self.id)


class Movement(db.Model):
    __tablename__ = 'movement'
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    name = Column(String, nullable=False)
    thumbnail = Column(String)
    category = Column(String)
    description = Column(Text)

    def __repr__(self):
        return '<Movement "{0}">'.format(self.name)

    @property
    def url(self):
        return url_for('wcal.movement_edit', id=self.id)