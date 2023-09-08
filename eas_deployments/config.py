import connexion
import pathlib
#from flask_cors import CORS
#from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from mongoengine import *


# contain the path for the connexion to the directory with our specifications
basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config['JWT_SECRET_KEY'] = ''
app.config['JWT_TOKEN_LOCATION'] = ''
app.config['MONGODB_SETTINGS'] = { # type: ignore
    'host': 'mongodb://localhost:27017/ecsdb'
    }
db = MongoEngine(app)