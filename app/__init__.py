from flask import Flask
from .controllers.auth.auth import auth_bp
from .controllers.user.user import user_bp 
from .controllers.profiles.profiles import prof_bp
from .controllers.camp_req.camp_req import camp_req
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "this_is_a_secret_key"

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(prof_bp)
        app.register_blueprint(camp_req)
        db.create_all()
        print ('table created')

    return app
