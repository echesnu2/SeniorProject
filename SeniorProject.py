from flask import Flask, render_template, request
from flask.ext.bcrypt import Bcrypt
import utilities
import amm_db

app = Flask(__name__)
app.debug = True
bcrypt = Bcrypt(app)

db = amm_db.AmmDB()


@app.route('/', methods=['GET', 'POST'])
def main_page():

    if request.method == 'POST':
        if request.form.get('email', None) is not None:
            db.add_user(fn=request.form['first_name'], ln=request.form['last_name'], email=request.form['email'],
                        uname=request.form['username'], passwd=bcrypt.generate_password_hash(request.form['password']))
        elif request.form.get('username-login', None) is not None:
            data = db.get_user(uname=request.form['username-login'], exact=True)

            print(len(data))

            if len(data) > 0:
                if bcrypt.check_password_hash(data[0]['passwd'], request.form['password-login']):
                    main_page()
                else:
                    return render_template('MainPage.html', error='Username/Password is incorrect')
            else:
                return render_template('MainPage.html', error='Username/Password is incorrect')

    return render_template('MainPage.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/create_event')
def create_event():
    return render_template('create_event.html', key=utilities.get_maps_key())

@app.route('/calendar')
def calendar():
    return render_template('SearchResultsPage.html')

@app.route('/rosters')
def rosters():
    return render_template('RostersPage.html')

if __name__ == '__main__':
    app.run()
