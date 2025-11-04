from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_blueprint = Blueprint('auth', __name__)

# signup (also /register)
@auth_blueprint.route('/register', methods=['GET', 'POST'])
@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        # already signed up?
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.')
            return redirect(url_for('auth.login'))

        # create -> save -> login -> go home
        u = User(email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u, remember=False)      # session cookie (ends on browser close)
        return redirect(url_for('main.todo'))

    return render_template('signup.html')

# login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # first run: if no users exist, go to signup
    if request.method == 'GET' and User.query.count() == 0:
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.')
            return render_template('login.html'), 401

        login_user(user, remember=False)   # session cookie (ends on browser close)
        return redirect(url_for('main.todo'))

    return render_template('login.html')

# logout
@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
