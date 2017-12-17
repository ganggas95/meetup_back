from flask import Flask, Blueprint
from meetup.api.restplus import restplus
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from meetup.config import initConfig
initConfig()
from meetup.model import table
from meetup.api.point import ns as point_service
from meetup.api.line import ns as line_service
from meetup.api.polygon import ns as polygon_service
blueprint = Blueprint('api', __name__, url_prefix='/service')
restplus.init_app(blueprint)
restplus.add_namespace(point_service)
restplus.add_namespace(line_service)
restplus.add_namespace(polygon_service)
app.register_blueprint(blueprint)


