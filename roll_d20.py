from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from sqlalchemy.orm import scoped_session

from db import get_session_factory
import models

app = Flask(__name__)
app.secret_key = 'v@p2rfNOa2j8Yci'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

session_factory = get_session_factory()
Session = scoped_session(session_factory)
session = Session()


@login_manager.user_loader
def load_user(user_id):
    user = session.query(models.UserModel).get(int(user_id))
    if user:
        return user
    else:
        return None


# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('campaigns.html', current_user=current_user)
    else:
        return render_template('home.html', current_user=current_user)


@app.route('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', current_user=current_user)


@app.route('/authenticate/', methods=['GET', 'POST'])
def authenticate():
    username = request.form.get('username', None)
    users = session.query(models.UserModel).filter(models.UserModel.username == username).all()
    if len(users) > 1:
        return abort(400)
    user = users[0]
    if user is not None and user.verify_password(request.form.get('password', None)):
        login_user(user)
        flash('You are now logged in. Welcome back!', 'success')
        return jsonify({"next": "/"})


@app.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/play_sessions/')
def play_sessions():
    if current_user.is_authenticated:
        return render_template('play_session.html', current_user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/exp_calculator/')
def exp_calculator():
    if current_user.is_authenticated:
        return render_template('exp_calculator.html', current_user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/probability/')
def probability():
    if current_user.is_authenticated:
        return render_template('probability.html', current_user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/grid_overlay/')
def grid_overlay():
    if current_user.is_authenticated:
        return render_template('grid_overlay.html', current_user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/player_feedback/')
def player_feedback():
    return render_template('player_feedback.html', current_user=current_user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
