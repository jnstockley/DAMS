from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src import dbCreds
import pymysql
from flask_login import LoginManager

pymysql.install_as_MySQLdb()

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.config["SECRET_KEY"] = "secret-key-goes-here"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql://{dbCreds.user}:{dbCreds.password}@{dbCreds.host}/{dbCreds.database}"

    db.init_app(app)

    # blueprint for auth routes in our app
    from src.account.register import register_blueprint as auth_blueprint
    from src.event.admin import admin_blueprint
    from src.login.login import login_blueprint
    from src.roles.receipient import request_blueprint
    from src.roles.donor import donor_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(request_blueprint)
    app.register_blueprint(donor_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = "login.login"

    from src.account.user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
