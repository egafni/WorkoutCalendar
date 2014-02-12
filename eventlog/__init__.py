

settings = dict(
    database_url = 'postgresql://egafni:lqsym@localhost/workout_calendar'
)


from .db import get_session

from models.event import Event

__all__ = ['Event', 'settings', 'get_session']