from ..db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, event, orm, PickleType, Text, Date, Time
import os
from flask import url_for
import datetime

opj = os.path.join

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    start = Column(DateTime, default=func.now())
    #date = Column(Date, nullable=False)
    #end = Column(DateTime, nullable=True)
    #time = Column(Time)
    #date_end = Column(Date)
    #time_end = Column(Time)
    name = Column(String, nullable=False)
    text = Column(Text)

    def date_isoformat(self):
        if self.time is None:
            return self.date.isoformat()
        else:
            return datetime.datetime.combine(self.date, self.time).isoformat()

    def __repr__(self):
        return '<Event "{0}">'.format(self.name, self.start.strftime('%Y-%m-%d'))
