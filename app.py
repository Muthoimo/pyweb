from flask import Flask

from blueprints.auth_blueprint import auth_views
from blueprints.main_blueprint import main_views

from flask_login import LoginManager
from models.database import user, User
from bson import ObjectId


app = Flask(__name__)

app.secret_key = "Enter your secret key"

#create routes.
app.register_blueprint(auth_views)
app.register_blueprint(main_views)

login = LoginManager(app)
login.login_view = "/login"

#Setup the login user loader.
@login.user_loader
def load_user(id):
    """Confirm user exists in database then use else return None"""
    cur_user = user.find_one({"_id": ObjectId(id)})

    if cur_user is None:
        return None

    # Create a user instance from the retrieved user.
    return User(cur_user.get("username"), str(cur_user.get("_id")))
