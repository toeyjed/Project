from main import main as main_blueprint
from auth import auth as auth_blueprint
from members import members as members_blueprint
# from covid import covid as covid_blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db,User
from flask_login import LoginManager


#Init SQLAlchemy 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'app-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()

#Register blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(members_blueprint)
# app.register_blueprint(covid_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)