from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin ,current_user
from flask import Blueprint, render_template
import requests

members = Blueprint('members', __name__)

db = SQLAlchemy()


class Members(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    studentid = db.Column(db.Integer())
    

@members.route('/about')
def about():
    return render_template('about.html', members = Members.query.all() , user=current_user)