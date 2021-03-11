from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,User
from flask_login import login_user, logout_user, login_required , current_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
   return render_template('login.html' ,user=current_user)

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    return redirect(url_for('main.covid'))

@auth.route('/signup')
def signup():
    return render_template('signup.html',user=current_user)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 

    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email,firstname=firstname,lastname=lastname,username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.covid') )
