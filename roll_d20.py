from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from sqlalchemy.orm import scoped_session
import datetime
import sys
from itertools import product

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


@app.route('/')
def home():
    #TODO create logged in home page
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
    username = request.values.get('username', None)
    users = session.query(models.UserModel).filter(models.UserModel.username == username).all()
    if len(users) > 1:
        return abort(400)
    user = users[0]
    if user is not None and user.verify_password(request.values.get('password', None)):
        login_user(user)
        flash('You are now logged in. Welcome back!', 'success')
        return jsonify({"next": "/"})
    else:
        return abort(400)


@app.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/campaigns/')
def campaigns():
    if current_user.is_authenticated:
        campaign_list = session.query(models.CampaignModel)\
            .filter(models.CampaignModel.user_id == current_user.id).all()
        return render_template('campaigns.html', current_user=current_user, campaigns=campaign_list)
    else:
        return redirect(url_for('login'))


@app.route('/campaigns/<campaign_id>/')
def play_sessions(campaign_id):
    if current_user.is_authenticated:
        campaign = session.query(models.CampaignModel).filter(models.CampaignModel.id == campaign_id).all()
        if len(campaign) > 1 or len(campaign) <= 0 or campaign[0].user_id != current_user.id:
            return abort(400)
        campaign = campaign[0]
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
        total_average, today_average = calculate_average()
        return render_template('probability.html', current_user=current_user, total_average=total_average,
                               today_average=today_average)
    else:
        return redirect(url_for('login'))


@app.route('/add_roll/', methods=['GET', 'POST'])
def add_roll():
    roll = int(request.values.get('roll', None))
    date = datetime.datetime.now().date()
    new_prob = models.ProbabilityModel()
    new_prob.date = date
    new_prob.roll = roll
    session.add(new_prob)
    session.commit()
    total_average, today_average = calculate_average()
    return jsonify({'total_average': total_average, 'today_average': today_average})


@app.route('/calculate_probability/', methods=['GET', 'POST'])
def calculate_probability():
    dice = dict()
    dice['four'] = request.values.get('4', None)
    dice['six'] = request.values.get('6', None)
    dice['eight'] = request.values.get('8', None)
    dice['ten'] = request.values.get('10', None)
    dice['twelve'] = request.values.get('12', None)
    dice['twenty'] = request.values.get('20', None)
    dice['one_hundred'] = request.values.get('100', None)
    target = int(request.values.get('target', None))
    odds = dice_probability(dice_list=dice, target=target)
    odds = odds * 100
    return jsonify({'probability': odds})


@app.route('/grid_overlay/')
def grid_overlay():
    if current_user.is_authenticated:
        return render_template('grid_overlay.html', current_user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/player_feedback/')
def player_feedback():

    if current_user.is_authenticated:
        campaign_list = session.query(models.CampaignModel).\
            filter(models.CampaignModel.user_id == current_user.id).all()
        info = dict()
        for campaign in campaign_list:
            list_feedback = session.query(models.PlayerFeedbackModel).filter(
                models.PlayerFeedbackModel.campaign_id == campaign.id)
            feedback = []
            for var in list_feedback:
                feedback.append(var)
            info[campaign.name] = feedback

        return render_template('player_feedback.html', current_user=current_user, info=info)
    else:
        campaign_list = session.query(models.CampaignModel).all()
        campaign_info = dict()
        for campaign in campaign_list:
            user = session.query(models.UserModel).get(campaign.user_id)
            user_name = user.name
            campaign_info[campaign.name] = user_name
        return render_template('feedback.html', current_user=current_user, campaigns=campaign_info)


@app.route('/submit_feedback/', methods=['GET', 'POST'])
def submit_feedback():
    campaign_name = request.values.get('campaign_name', None)
    # campaign_owner = request.values.get('campaign_owner', None)
    player_name = request.values.get('player_name', None)
    try:
        date = datetime.datetime.strptime(request.values.get('date', None), '%m-%d-%Y')
    except Exception as e:
        return abort(400, message="Invalid Date")

    feedback = request.values.get('feedback', None)
    campaign = session.query(models.CampaignModel).filter(models.CampaignModel.name == campaign_name).all()
    if len(campaign) != 1:
        return abort(400, message="Error with finding campaign with name: {}".format(campaign_name))
    new_feedback = models.PlayerFeedbackModel()
    new_feedback.campaign_id = campaign[0].id
    new_feedback.date = date
    new_feedback.player_name = player_name
    new_feedback.feedback = feedback
    session.add(new_feedback)
    session.commit()
    return jsonify({"success": "Successfully submitted feedback"})


def calculate_average():
    all_probability = session.query(models.ProbabilityModel).all()
    total_rolls = len(all_probability)
    total_sum = 0
    if total_rolls != 0:
        for roll in all_probability:
            total_sum += roll.roll
        total_average = total_sum / total_rolls
    else:
        total_average = 0
    today = datetime.datetime.now().date()
    today_probability = session.query(models.ProbabilityModel).filter(models.ProbabilityModel.date == today).all()
    today_total_rolls = len(today_probability)
    today_sum = 0
    if today_total_rolls != 0:
        for roll in today_probability:
            today_sum += roll.roll
        today_average = today_sum / today_total_rolls
    else:
        today_average = 0
    return total_average, today_average


def dice_probability(dice_list, target):
    product_list = []
    for key, value in dice_list.items():
        sides = 0
        if key == 'four':
            sides = 4
        if key == 'six':
            sides = 6
        if key == 'eight':
            sides = 8
        if key == 'ten':
            sides = 10
        if key == 'twelve':
            sides = 12
        if key == 'twenty':
            sides = 20
        if key == 'one_hundred':
            sides = 100

        dice_number = int(value)
        for i in range(1, dice_number + 1):
            add = ()
            for j in range(1, sides+1):
                add += (j,)
            product_list.append(add)

    rollAmount = 0
    targetAmount = 0
    products = product(*product_list)
    for i in products:
        thisSum = 0
        rollAmount += 1
        for j in i:
            thisSum += j
        if thisSum >= target:
            targetAmount += 1
    odds = targetAmount / rollAmount
    return odds


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
