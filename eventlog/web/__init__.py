from . import filters
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .views import gen_bprint
from .. import settings


fapp = Flask(__name__)
fapp.config['DEBUG'] = True
fapp.config['SECRET_KEY'] = 'ASDFASFSD'
fapp.config['SQLALCHEMY_DATABASE_URI'] = settings['database_url']
_db = SQLAlchemy(fapp)
session = _db.session


def runweb(host, port):
    """
    start the flask development webserver
    """
    from . import views

    fapp.run(debug=True, host=host, port=port)

bprint = gen_bprint(session)
filters.add_to_bprint(bprint)
fapp.register_blueprint(bprint)
