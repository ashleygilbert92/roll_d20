import datetime
import re

from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from itertools import product
from werkzeug.security import generate_password_hash

import models
from db import get_session_factory

app = Flask(__name__)
app.secret_key = 'v@p2rfNOa2j8Yci'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

Session = get_session_factory()


@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(models.UserModel).get(int(user_id))
    if user:
        return user
    else:
        return None


@app.route('/')
def home():
    #TODO create logged in home page
    if current_user.is_authenticated:
        return redirect(url_for('campaigns'))
    else:
        return render_template('home.html', current_user=current_user)


@app.route('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', current_user=current_user)


@app.route('/sign_up/')
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('sign_up.html', current_user=current_user)


@app.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    name = request.values.get('full_name', None)
    username = request.values.get('username', None)
    regex = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not regex.match(username):
        return abort(400)
    password = generate_password_hash(request.values.get('password'))

    session = Session()
    new_user = models.UserModel()
    new_user.name = name
    new_user.username = username
    new_user.password = password
    session.add(new_user)
    session.commit()
    login_user(new_user)
    return jsonify({"next": "/"})


@app.route('/authenticate/', methods=['GET', 'POST'])
def authenticate():
    session = Session()
    username = request.values.get('username', None)
    users = session.query(models.UserModel).filter(models.UserModel.username == username).all()
    if len(users) > 1:
        return abort(400)
    user = users[0]
    if user is not None and user.verify_password(request.values.get('password', None)):
        login_user(user)
        return jsonify({"next": "/"})
    else:
        return abort(400)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/campaigns/')
def campaigns():
    if current_user.is_authenticated:
        session = Session()
        campaign_list = session.query(models.CampaignModel)\
            .filter(models.CampaignModel.user_id == current_user.id).all()
        return render_template('campaigns.html', current_user=current_user, campaigns=campaign_list)
    else:
        return redirect(url_for('sign_up'))


@app.route('/add_campaign/', methods=['GET', 'POST'])
def add_campaign():
    if current_user.is_authenticated:
        name = request.values.get('name', None)
        if name is "":
            return abort(404)

        session = Session()
        new_campaign = models.CampaignModel()
        new_campaign.user_id = current_user.id
        new_campaign.name = name
        session.add(new_campaign)
        session.commit()
        return jsonify({"next": "/campaigns/{}/".format(new_campaign.id)})
    else:
        return abort(401)


@app.route('/campaigns/<campaign_id>/')
def play_sessions(campaign_id):
    if current_user.is_authenticated:
        session = Session()
        campaign = session.query(models.CampaignModel).get(campaign_id)
        if campaign is None:
            return abort(404)
        if campaign.user_id != current_user.id:
            return abort(401)
        play_session_list = session.query(models.PlaySessionModel).\
            filter(models.PlaySessionModel.campaign_id == campaign.id).all()
        players_list = session.query(models.PlayerModel).filter(models.PlayerModel.campaign_id == campaign.id).all()
        return render_template('play_sessions.html', current_user=current_user,
                               play_sessions=play_session_list, campaign=campaign, players=players_list)
    else:
        return redirect(url_for('sign_up'))


@app.route('/add_play_session/', methods=['GET', 'POST'])
def add_play_session():
    if current_user.is_authenticated:
        campaign_id = int(request.values.get('campaign_id', None))
        try:
            date = datetime.datetime.strptime(request.values.get('date', None), '%Y-%m-%d')
        except Exception as e:
            return abort(404, message="Invalid Date")
        description = request.values.get('description', None)

        session = Session()
        new_play_session = models.PlaySessionModel()
        new_play_session.campaign_id = campaign_id
        new_play_session.date = date
        new_play_session.description = description
        session.add(new_play_session)
        session.commit()
        return jsonify({"next": "/play_sessions/{}/".format(new_play_session.id)})
    else:
        return abort(401)


@app.route('/add_player/', methods=['GET', 'POST'])
def add_player():
    if current_user.is_authenticated:
        campaign_id = int(request.values.get('campaign_id', None))
        name = request.values.get('name', None)
        class1 = request.values.get('class1', None)
        class2 = request.values.get('class2', None)
        level = int(request.values.get('level', None))
        mythic_tier = request.values.get('mythic_tier', None)
        exp = int(request.values.get('exp', None))

        if mythic_tier is None or mythic_tier is "":
            mythic_tier = 0
        else:
            mythic_tier = int(mythic_tier)

        session = Session()
        new_player = models.PlayerModel()
        new_player.campaign_id = campaign_id
        new_player.name = name
        new_player.class1 = class1
        new_player.class2 = class2
        new_player.level = level
        new_player.mythic_tier = mythic_tier
        new_player.exp = exp
        session.add(new_player)
        session.commit()
        return jsonify({"next": "/campaigns/{}/".format(campaign_id)})
    else:
        return abort(401)


@app.route('/get_player/', methods=['GET', 'POST'])
def get_player():
    if current_user.is_authenticated:
        player_id = int(request.values.get('player_id', None))
        session = Session()
        player = session.query(models.PlayerModel).get(player_id)
        return jsonify({"player": {
            "id": player.id,
            "campaign_id": player.campaign_id,
            "name": player.name,
            "class1": player.class1,
            "class2": player.class2,
            "level": player.level,
            "mythic_tier": player.mythic_tier,
            "exp": player.exp
        }})
    else:
        return abort(401)


@app.route('/edit_player/', methods=['GET', 'PUT'])
def edit_player():
    if current_user.is_authenticated:
        campaign_id = int(request.values.get('campaign_id', None))
        player_id = int(request.values.get('player_id', None))
        name = request.values.get('name', None)
        class1 = request.values.get('class1', None)
        class2 = request.values.get('class2', None)
        level = int(request.values.get('level', None))
        mythic_tier = request.values.get('mythic_tier', None)
        exp = int(request.values.get('exp', None))

        if mythic_tier is None or mythic_tier is "":
            mythic_tier = 0
        else:
            mythic_tier = int(mythic_tier)

        session = Session()
        player = session.query(models.PlayerModel).filter(models.PlayerModel.campaign_id == campaign_id)\
            .filter(models.PlayerModel.id == player_id).one()
        player.campaign_id = campaign_id
        player.name = name
        player.class1 = class1
        player.class2 = class2
        player.level = level
        player.mythic_tier = mythic_tier
        player.exp = exp
        # session.add(player)
        session.commit()
        return jsonify({"next": "/campaigns/{}/".format(campaign_id)})
    else:
        return abort(401)


@app.route('/play_sessions/<session_id>/')
def encounters(session_id):
    if current_user.is_authenticated:
        session = Session()
        play_session = session.query(models.PlaySessionModel).get(session_id)
        if play_session is None:
            return abort(404)
        campaign_id = play_session.campaign_id
        campaign = session.query(models.CampaignModel).get(campaign_id)
        if campaign is None:
            return abort(404)
        if campaign.user_id != current_user.id:
            return abort(401)
        encounters_list = session.query(models.EncounterModel).\
            filter(models.EncounterModel.session_id == session_id).all()
        session_notes_list = session.query(models.SessionNoteModel).\
            filter(models.SessionNoteModel.session_id == session_id)
        return render_template('encounters.html', current_user=current_user,
                               play_session=play_session, encounters=encounters_list, session_notes=session_notes_list)
    else:
        return redirect(url_for('sign_up'))


@app.route('/add_session_notes/', methods=['GET', 'POST'])
def session_notes():
    if current_user.is_authenticated:
        session_id = int(request.values.get('session_id', None))
        notes = request.values.get('notes', None)
        r = '<br />'
        notes = notes.replace('\n', r)

        session = Session()
        new_session_note = models.SessionNoteModel()
        new_session_note.session_id = session_id
        new_session_note.notes = notes
        session.add(new_session_note)
        session.commit()
        return jsonify({"next": "/play_sessions/{}/".format(session_id)})
    else:
        return abort(401)


@app.route('/get_note/', methods=['GET', 'POST'])
def get_note():
    if current_user.is_authenticated:
        note_id = int(request.values.get('note_id', None))
        session = Session()
        note = session.query(models.SessionNoteModel).get(note_id)
        notes = note.notes
        r = '\n'
        notes = notes.replace('<br />', r)
        return jsonify({"note": {
            "id": note.id,
            "session_id": note.session_id,
            "notes": notes
        }})
    else:
        return abort(401)


@app.route('/edit_session_notes/', methods=['GET', 'PUT'])
def edit_session_notes():
    if current_user.is_authenticated:
        note_id = int(request.values.get('note_id', None))
        session_id = int(request.values.get('session_id', None))
        notes = request.values.get('notes', None)
        r = '<br />'
        notes = notes.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

        session = Session()
        edit_session_note = session.query(models.SessionNoteModel)\
            .filter(models.SessionNoteModel.session_id == session_id)\
            .filter(models.SessionNoteModel.id == note_id).one()
        edit_session_note.session_id = session_id
        edit_session_note.notes = notes
        # session.add(edit_session_note)
        session.commit()
        return jsonify({"next": "/play_sessions/{}/".format(session_id)})
    else:
        return abort(401)


@app.route('/add_encounter/', methods=['GET', 'POST'])
def add_encounter():
    if current_user.is_authenticated:
        session_id = int(request.values.get('session_id', None))
        name = request.values.get('name', None)
        description = request.values.get('description', None)

        session = Session()
        new_encounter = models.EncounterModel()
        new_encounter.session_id = session_id
        new_encounter.name = name
        new_encounter.description = description
        session.add(new_encounter)
        session.commit()
        return jsonify({"next": "/encounters/{}/".format(new_encounter.id)})
    else:
        return abort(401)


@app.route('/encounters/<encounter_id>/')
def encounter_actions(encounter_id):
    if current_user.is_authenticated:
        session = Session()
        encounter = session.query(models.EncounterModel).get(encounter_id)
        if encounter is None:
            return abort(404)
        session_id = encounter.session_id
        play_session = session.query(models.PlaySessionModel).get(session_id)
        if play_session is None:
            return abort(404)
        campaign_id = play_session.campaign_id
        campaign = session.query(models.CampaignModel).get(campaign_id)
        if campaign is None:
            return abort(404)
        if campaign.user_id != current_user.id:
            return abort(401)
        encounters_actions_list = session.query(models.EncounterActionModel).\
            filter(models.EncounterActionModel.encounter_id == encounter_id).all()
        players_list = session.query(models.PlayerModel).filter(models.PlayerModel.campaign_id == campaign.id)
        return render_template('encounter_actions.html', current_user=current_user,
                               encounter=encounter, encounter_actions=encounters_actions_list, players=players_list)
    else:
        return redirect(url_for('sign_up'))


@app.route('/add_encounter_action/', methods=['GET', 'POST'])
def add_encounter_action():
    if current_user.is_authenticated:
        encounter_id = int(request.values.get('encounter_id', None))
        player_id = int(request.values.get('player_id', None))
        damage_taken = request.values.get('damage_taken', None)
        damage_done = request.values.get('damage_done', None)
        # spells_cast = int(request.values.get('spells_cast', None))
        healing = request.values.get('healing', None)

        if damage_taken is None or damage_taken is "":
            damage_taken = 0
        else:
            damage_taken = int(damage_taken)

        if damage_done is None or damage_done is "":
            damage_done = 0
        else:
            damage_done = int(damage_done)

        if healing is None or healing is "":
            healing = 0
        else:
            healing = int(healing)

        session = Session()
        new_encounter_action = models.EncounterActionModel()
        new_encounter_action.encounter_id = encounter_id
        new_encounter_action.player_id = player_id
        new_encounter_action.damage_taken = damage_taken
        new_encounter_action.damage_done = damage_done
        # new_encounter_action.spells_cast = spells_cast
        new_encounter_action.healing = healing
        session.add(new_encounter_action)
        session.commit()
        return jsonify({"next": "/encounters/{}/".format(encounter_id)})
    else:
        return abort(401)


@app.route('/get_encounter_action/', methods=['GET', 'POST'])
def get_encounter_action():
    if current_user.is_authenticated:
        action_id = int(request.values.get('action_id', None))
        session = Session()
        action = session.query(models.EncounterActionModel).get(action_id)
        return jsonify({"encounter_action": {
            "id": action.id,
            "encounter_id": action.encounter_id,
            "player_id": action.player_id,
            "damage_taken": action.damage_taken,
            "damage_done": action.damage_done,
            # "spells_cast": action.spells_cast,
            "healing": action.healing
        }})
    else:
        return abort(401)


@app.route('/edit_encounter_action/', methods=['GET', 'PUT'])
def edit_encounter_action():
    if current_user.is_authenticated:
        encounter_action_id = int(request.values.get('encounter_action_id', None))
        encounter_id = int(request.values.get('encounter_id', None))
        player_id = int(request.values.get('player_id', None))
        damage_taken = request.values.get('damage_taken', None)
        damage_done = request.values.get('damage_done', None)
        # spells_cast = int(request.values.get('spells_cast', None))
        healing = request.values.get('healing', None)

        if damage_taken is None or damage_taken is "":
            damage_taken = 0
        else:
            damage_taken = int(damage_taken)

        if damage_done is None or damage_done is "":
            damage_done = 0
        else:
            damage_done = int(damage_done)

        if healing is None or healing is "":
            healing = 0
        else:
            healing = int(healing)

        session = Session()
        new_edit_encounter_action = session.query(models.EncounterActionModel)\
            .filter(models.EncounterActionModel.encounter_id == encounter_id)\
            .filter(models.EncounterActionModel.player_id == player_id)\
            .filter(models.EncounterActionModel.id == encounter_action_id).one()
        new_edit_encounter_action.encounter_id = encounter_id
        new_edit_encounter_action.player_id = player_id
        new_edit_encounter_action.damage_taken = damage_taken
        new_edit_encounter_action.damage_done = damage_done
        # new_edit_encounter_action.spells_cast = spells_cast
        new_edit_encounter_action.healing = healing
        # session.add(new_edit_encounter_action)
        session.commit()
        return jsonify({"next": "/encounters/{}/".format(encounter_id)})
    else:
        return abort(401)


@app.route('/exp_calculator/')
def exp_calculator():
    if current_user.is_authenticated:
        return render_template('exp_calculator.html', current_user=current_user)
    else:
        return redirect(url_for('sign_up'))


@app.route('/probability/')
def probability():
    if current_user.is_authenticated:
        total_average, today_average = calculate_average()
        return render_template('probability.html', current_user=current_user, total_average=total_average,
                               today_average=today_average)
    else:
        return redirect(url_for('sign_up'))


@app.route('/add_roll/', methods=['GET', 'POST'])
def add_roll():
    if current_user.is_authenticated:
        roll = int(request.values.get('roll', None))
        date = datetime.datetime.now().date()
        new_prob = models.ProbabilityModel()
        new_prob.date = date
        new_prob.roll = roll

        session = Session()
        session.add(new_prob)
        session.commit()
        total_average, today_average = calculate_average()
        return jsonify({'total_average': total_average, 'today_average': today_average})
    else:
        return abort(401)


@app.route('/calculate_probability/', methods=['GET', 'POST'])
def calculate_probability():
    if current_user.is_authenticated:
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
    else:
        return abort(401)


@app.route('/grid_overlay/')
def grid_overlay():
    if current_user.is_authenticated:
        return render_template('grid_overlay.html', current_user=current_user)
    else:
        return redirect(url_for('sign_up'))


@app.route('/player_feedback/')
def player_feedback():
    if current_user.is_authenticated:
        session = Session()
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
        session = Session()
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
        date = datetime.datetime.strptime(request.values.get('date', None), '%Y-%m-%d')
    except Exception as e:
        return abort(400, message="Invalid Date")
    session = Session()
    feedback = request.values.get('feedback', None)
    r = '<br />'
    feedback = feedback.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

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
    session = Session()
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

    roll_amount = 0
    target_amount = 0
    products = product(*product_list)
    for i in products:
        this_sum = 0
        roll_amount += 1
        for j in i:
            this_sum += j
        if this_sum >= target:
            target_amount += 1
    odds = target_amount / roll_amount
    return odds


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
