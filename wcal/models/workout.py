from ..db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, event, orm, PickleType, Text, Date, Time
import os
from flask import url_for

opj = os.path.join


def default_task_log_output_dir(task):
    return opj(task.execution.output_dir, 'log', task.stage.name, task.tags_as_query_string())
def default_task_output_dir(task):
    return opj(task.execution.output_dir, task.stage.name, task.tags_as_query_string())


class WorkoutSession(Base):
    __tablename__ = 'workout_session'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    start = Column(Date, nullable=False)
    end = Column(Date)
    time = Column(Time)
    title = Column(String, nullable=False)
    text = Column(Text)
    def __repr__(self):
        return '<WorkoutSession "{0}">'.format(self.title, self.start.strftime('%Y-%m-%d'))
