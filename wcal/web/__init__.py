from flask import Flask
from views import bprint
import filters

def runweb(host, port):
    """
    start the flask development webserver
    """
    from . import views
    flask_app = Flask(__name__)
    flask_app.register_blueprint(bprint)
    flask_app.config['DEBUG'] = True
    flask_app.config['SECRET_KEY'] = 'ASDFASFSD'

    flask_app.run(debug=True, host=host, port=port)


