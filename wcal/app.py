from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

flask_app = Flask(__name__, static_folder='web/static')
flask_app.config['DEBUG'] = True
flask_app.config['SECRET_KEY'] = 'ASDFASFSD'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/erik/wcal.sqlite'
flask_app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(flask_app)
session = db.session

db = db
session = session


def reset_db():
    db.drop_all()
    db.create_all()

def runweb(host, port):
    """
    start the flask development webserver
    """
    for rule in flask_app.url_map.iter_rules():
        print rule.rule

    flask_app.run(debug=True, host=host, port=port)