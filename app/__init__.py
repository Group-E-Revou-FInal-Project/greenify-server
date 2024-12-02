
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Define basic routes for DB creation and seeding
    @app.route('/')
    def index():
       return 'HELLO WORLD'
    
    return app
