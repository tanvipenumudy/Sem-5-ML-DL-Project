from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session, Blueprint, make_response, jsonify, json
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
# from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
Bootstrap(app)

db = SQLAlchemy()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
        return render_template("profile.html", name=current_user.name, cname=current_user.cname)

@app.route('/tests', methods=['GET', 'POST'])
@login_required
def tests():
    return render_template('tests.html')

def create_app():

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    app_blueprint = Blueprint('app', __name__)
    app.register_blueprint(app_blueprint)
    return app

def run_app():
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    run_app()
