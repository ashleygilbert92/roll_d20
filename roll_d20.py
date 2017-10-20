from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, current_user
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.secret_key = 'v@p2rfNOa2j8Yci'
login_manager = LoginManager()
login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     # return User.get(user_id)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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


@app.route('/logout/')
def logout():
    """some stuff"""


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
