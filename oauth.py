from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from oauth import OAuthSignIn
from stravalib.client import Client
import requests


app = Flask(__name__)

app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'strava': {
        'id': 'xxx',
        'secret': 'xxx'
    },
    'twitter': {
        'id': 'xxx',
        'secret': 'xxx'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    twitter_id = db.Column(db.String(64), nullable=False)    
    email = db.Column(db.String(64), nullable=True)
    strava_id = db.Column(db.String(255), nullable=True)
    strava_access_code = db.Column(db.String(255), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/token_exchange', methods=["GET","POST"])
def token_exchange():
    mycode = request.args.get('code')
    strava_client_id = 'xxx'
    strava_client_secret = 'xxx'

    strava_token_uri = 'https://www.strava.com/oauth/token'
    params = {'client_id' : strava_client_id, 'client_secret' : strava_client_secret,'code' : mycode}
    res = requests.post(strava_token_uri, params)
    return res.text

@app.route('/authorize/strava')
def authorize_strava():
    strava_client_id = "xxx"
    strava_login_uri = "https://www.strava.com/oauth/authorize?client_id="+strava_client_id+"&response_type=code&redirect_uri=http://127.0.0.1:5000/token_exchange&approval_prompt=force"
    return redirect (strava_login_uri)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()


    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    user = User.query.filter_by(social_id=social_id).first()

    if not user:
        user = User(social_id=social_id, twitter_id=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
