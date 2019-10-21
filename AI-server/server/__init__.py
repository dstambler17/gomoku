from flask import Flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

mongo = PyMongo()
def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["MONGO_URI"] = "mongodb://localhost:27017/GomokuGame"
    mongo.init_app(app)

    from server.Gomoku.views import Gomoku
    app.register_blueprint(Gomoku, url_prefix='/gomoku')

    return app
