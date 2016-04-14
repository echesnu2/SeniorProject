from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask.ext.bcrypt import Bcrypt
import utilities
import amm_db
import datetime
import calendar
import time

app = Flask(__name__)
app.debug = True
bcrypt = Bcrypt(app)
app.secret_key = 'test'

db = amm_db.AmmDB('ammdb.cwwnkw8gimhn.us-west-2.rds.amazonaws.com', 'adminadmin')


@app.route('/', methods=['GET', 'POST'])
def main_page():
    session['userID'] = None
    db.get_last_id()
    if request.method == 'POST':
        if request.form.get('email', None) is not None:
            db.add_user(fn=request.form['first_name'], ln=request.form['last_name'], email=request.form['email'],
                        uname=request.form['username'], passwd=bcrypt.generate_password_hash(request.form['password']))
        elif request.form.get('username-login', None) is not None:
            data = db.get_user(uname=request.form['username-login'], exact=True)

            if len(data) > 0:
                if bcrypt.check_password_hash(data[0]['passwd'], request.form['password-login']):
                    user_id = data[0]['id']
                    session['user_id'] = user_id
                    return redirect(url_for('home'))

                else:
                    return render_template('MainPage.html', error='Username/Password is incorrect')
            else:
                return render_template('MainPage.html', error='Username/Password is incorrect')

    return render_template('MainPage.html')


@app.route('/home')
def home():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    else:
        user_info = db.get_user(session.get('user_id'))
        return render_template('home.html', user=user_info)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    else:
        user_info = db.get_user(session.get('user_id'))
        if request.method == 'POST':
            response = 'Passwords do not match!'
            if request.form['password'] != request.form['c_password']:
                return render_template('profile.html', user=user_info, response=response, css_class='red-text')
            else:
                if request.form['password'] != '':
                    db.edit_user(session.get('user_id'), email=request.form['u_email'],
                                 fname=request.form['fname'], lname=request.form['lname'],
                                 passwd=bcrypt.generate_password_hash(request.form['password']),
                                 phone=request.form['phone'])
                else:
                    db.edit_user(session.get('user_id'), email=request.form['u_email'],
                                 fname=request.form['fname'], lname=request.form['lname'],
                                 passwd='', phone=request.form['phone'])

                response = 'Updates made to profile!'
                user_info = db.get_user(session.get('user_id'))

                return render_template('profile.html', response=response, css_class='green-text', user=user_info)
        else:
            return render_template('profile.html', user=user_info)


@app.route('/create_event', methods=['POST', 'GET'])
def create_event():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    user_info = db.get_user(session.get('user_id'))
    categories = db.get_activity_type()

    if request.method == 'POST':
        activity_name = request.form['activity-name']
        category = request.form['category']
        private = request.form['private']
        date = request.form['date']
        time = request.form['time']
        duration = request.form['duration']
        latitude = request.form['lat']
        longitude = request.form['lng']
        num_of_players = request.form['num-of-players']
        skill = request.form['skill-level']
        datetime = utilities.combine_datetime(date, time)

        db.add_activity(name=activity_name, category=category, datetime=datetime, duration=duration, latitude=latitude,
                        longitude=longitude, numplayers=num_of_players, skill=skill, private=private, leader=session.get
                        ('user_id'), available=1)
        db.add_user_activity(session.get('user_id'), db.get_activity(name=activity_name, category=category, skill=skill,
                                                                     leader=session.get('user_id')))
        redirect(url_for('home'))

    return render_template('create_event.html', key=utilities.get_key('google_maps'), user=user_info,
                           categories=categories)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    user_info = db.get_user(session.get('user_id'))
    categories = db.get_activity_type()

    if request.method == 'POST':
        if request.form.get('join', None) is None:
            activity_name = request.form['activity-name']
            results = db.get_activity(name=activity_name)
            return render_template('SearchResultsPage.html', user=user_info, results=results, categories=categories,
                                   maps_key=utilities.get_key('google_maps'))
        else:
            db.add_user_activity(user_info[0]['id'], request.form['activity-id'])
            utilities.send_email(user_info[0]['email'], 'Activity Joined', 'You joined: ' +
                                 request.form['activity-name-item'])

            return render_template('SearchResultsPage.html', user=user_info, categories=categories,
                                   maps_key=utilities.get_key('google_maps'))
    else:
        return render_template('SearchResultsPage.html', user=user_info, categories=categories,
                               maps_key=utilities.get_key('google_maps'))


@app.route('/calender')
def calender():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    user_info = db.get_user(session.get('user_id'))
    date = calendar.Calendar(6).monthdatescalendar(datetime.datetime.utcnow().year, datetime.datetime.utcnow().month)

    act_list = []
    activities = db.get_user_activity(user_id=user_info[0]['id'])
    for activity in activities:
        activity_details = db.get_activity(activity_id=activity['activityid'])[0]
        activity_details['latitude'] = float(activity_details['latitude'])
        activity_details['longitude'] = float(activity_details['longitude'])
        activity_details['time'] = int(time.mktime(activity_details['datetime'].timetuple())) * 1000
        act_list.append(activity_details)

    return render_template('calender.html', user=user_info, date=date, activities=act_list,
                           maps_key=utilities.get_key('google_maps'))


@app.route('/rosters', methods=['GET', 'POST'])
def rosters():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    user_info = db.get_user(session.get('user_id'))

    act_list = []
    activities = db.get_user_activity(user_id=user_info[0]['id'])
    for activity in activities:
        activity_details = db.get_activity(activity_id=activity['activityid'])[0]
        activity_details['latitude'] = float(activity_details['latitude'])
        activity_details['longitude'] = float(activity_details['longitude'])
        activity_details['time'] = int(time.mktime(activity_details['datetime'].timetuple())) * 1000
        activity_details['date'] = activity_details['datetime'].date().strftime('%m/%d/%Y')
        act_list.append(activity_details)

    if request.method == 'GET':
        if request.args.get('loadActivityID') is not None:
            print(request.args['loadActivityID'])
            user_activity = db.get_user_activity(activity_id=request.args['loadActivityID'])

            users = []
            for record in user_activity:
                user = db.get_user(user_id=record['userid'], select='id, uname')[0]
                user['approved'] = record['isApplicant']
                users.append(user)
            print(users)
            return jsonify(users=users)

    return render_template('RostersPage.html', user=user_info, activities=act_list,
                           maps_key=utilities.get_key('google_maps'))

@app.route('/logout')
def logout():
    if session.get('user_id', None) is None:
        return redirect(url_for('main_page'))
    session.clear()
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run()
