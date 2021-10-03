from flask import Flask, redirect, render_template, request, url_for, session, jsonify, send_file
from requests_oauthlib import OAuth2Session

import json, os, time, pymongo


# <- Config ->

api_auth_key = """LjtQYLaGbgZPTmEy@H%R^ZS=mG44+nLaPZUgaFv8qLJ#P8&fPq$_5FuW^Ep&%Juyg&?&X=+ub!DeV#w!WR!venshQ3NkskNUqnvjBf+^*t+_gvN?2TvyAF#nYv9x8Wmy*FYzJX$fh5Zx%M!n_q9tL-yh?t@tSu!xSCZvk&qzDqDsDkcWTxz^3k5$T*NxENmAd^*+S%!PMkauCpBWZ3fNsKd+csbWY$BHSh+%chwvB=MRVZE#J4Un_Wp$H?rAk66z"""
client_secret = """$3ZKcfybdwqD$BV=N*M@_&KYJ2N4wcK*6v3?%mLtYN$rr=NUm#aeLbr!8jhvhPCv5AtNwvUGemx@KBS&+cSYXHJgj_-6RfTewf6Kg-s=5TcX=a%Pvjj8TgF%Uf$JWP4$T_g2AvHNLaR4nMS&pvj9^8JJQc+yRR5XGj!sQTJD7BLDPfk*V9Yy68NacAk^vv@&MXk%G?uTE=Y@ur7tYnm=pknnF5syWWf7g2W&5$+UZ8cR=w*72qSgJPN!9fE=HWdJ"""

client_id = 875452721199726663
client_secret = "b5U-nzXLThNJRdQpWeEiJmEVSipaEWiJ"
redirect_uri = "http://localhost:5000/callback"


# <---     Flask     --->

app = Flask(__name__)

app.config['SECRET_KEY'] = client_secret


# <---     Discord Oauth2 Setup     --->

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

OAUTH2_CLIENT_ID = client_id
OAUTH2_CLIENT_SECRET = client_secret
OAUTH2_REDIRECT_URI = redirect_uri

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


# <---     Secret Setting     --->

API_AUTHENTICATION_KEY = api_auth_key

# <---     Functions     --->

def make_discord_session(session):
    try:
        discord = make_session(token=session.get('oauth2_token'))

        user = discord.get(API_BASE_URL + '/users/@me').json()
        guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()

        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"

        test = user["username"]

        data = {"logged_in": True, "user": user, "guilds": guilds}

        return data
    except:
        data = {"logged_in": False}

        return data

# <---     Main Pages     --->

@app.route("/")
def index():
    discord_session_data = make_discord_session(session)

    return render_template("index.html", logged_in = discord_session_data["logged_in"], data = discord_session_data)

# <---     Discord Oauth2     --->

@app.route('/login')
def login():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        name = user["username"]
        return redirect("/serverselect")
    except:
        issignedin = False

    scope = request.args.get(
        'scope',
        'identify email guilds')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    try:
        if request.values.get('error'):
            return request.values['error']
        discord = make_session(state=session.get('oauth2_state'))
        token = discord.fetch_token(
            TOKEN_URL,
            client_secret=OAUTH2_CLIENT_SECRET,
            authorization_response=request.url)
        session['oauth2_token'] = token
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()

        return redirect("/"), 302
    except:
        return 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/"), 302

# <---     Run Server     --->

if __name__ == "__main__":
    app.run(debug=True)
