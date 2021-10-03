from flask import Flask, redirect, render_template, request, url_for, g, session, jsonify, send_file
from requests_oauthlib import OAuth2Session
from flask_socketio import SocketIO, emit
import json, os, time

OAUTH2_CLIENT_ID = "no"
OAUTH2_CLIENT_SECRET = "no"
OAUTH2_REDIRECT_URI = 'http://localhost:5000/discord-callback' #https://bobadankers.xyz//discord-callback http://localhost:5000/discord-callback

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

BOT_AUTH_KEY = "*&T&tn6tn897m9ymhuhhihimnNY^BB^MM7789m89u008977809789765656IM<UHTY(*&^%^*)"

dankinforequests = []
dankinforequestsreturn = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
socketio = SocketIO(app)

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

#                 MAIN PAGES

@app.route('/')
def home():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
        discrim = user["discriminator"]
        issignedin = True
    except:
        pfp = None
        name = None
        discrim = None
        issignedin = False

    userdata = {"pfp": pfp, "name": name, "discrim": discrim}

    return render_template("home.html", userdata=userdata, issignedin=issignedin)

@app.route('/dashboard')
def dashboard():
    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        if "c_" in user['avatar']:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
        discrim = user["discriminator"]
        id = user["id"]
    except:
        return redirect("/")

    with open("data/server-info.json") as f:
        serverinfo = json.load(f)
        f.close()

    with open("data/user-dank-info.json") as f:
        dankinfo = json.load(f)
        f.close()

    try:
        dankinfo = dankinfo[str(id)]
        indankdata = True
    except:
        indankdata = False

    if indankdata:
        wallet = dankinfo["bal"]["wallet"]
        bank = dankinfo["bal"]["bank"]

        dankinfo["bal"]["wallet"] = f"{wallet:,}"
        dankinfo["bal"]["bank"] = f"{bank:,}"


    userdata = {"pfp": pfp, "name": name, "discrim": discrim, "id": id}

    return render_template("dashboard.html", userdata=userdata, serverinfo=serverinfo, dankinfo=dankinfo, indankdata=indankdata)

@app.route("/help/cookies")
def cookieredirect():
    return redirect("https://www.cookiepolicygenerator.com/live.php?token=VknyM1lNqLfHxsAtp2usHrafGZXB7zb7")

#                 WEBSITE SOCKET PINGS

@socketio.on('update dank data')
def update_dank(message):
    global dankinforequests, dankinforequestsreturn
    if message['id'] not in dankinforequests:
        dankinforequests.append(message['id'])

    while message["id"] not in dankinforequestsreturn:
        time.sleep(2)

    socketio.emit('dank data return', dankinforequestsreturn[message["id"]])

    with open("data/user-dank-info.json") as f:
        dankinfo = json.load(f)
        f.close()

    dankinfo[message["id"]] = {"bal": {}}

    dankinfo[message["id"]]["bal"]["wallet"] = dankinforequestsreturn[message["id"]][0]
    dankinfo[message["id"]]["bal"]["bank"] = dankinforequestsreturn[message["id"]][1]

    with open("data/user-dank-info.json", "w+") as f:
        json.dump(dankinfo, f)
        f.close()

    del dankinforequestsreturn[message["id"]]

@socketio.on('request announcements')
def update_dank(message):
    socketio.emit('dank data return', dankinforequestsreturn[message["id"]])

@socketio.on('connect')
def connect():
    print("Client connected!")

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected!')

#                 DANK MEMER DATA

@app.route("/request-dank-requests", methods=["GET"])
def dankrequests():
    global dankinforequests
    try:
        if request.headers["password"] != BOT_AUTH_KEY:
            return jsonify({"message": "Header 'password' incorrect!"})
    except KeyError:
        return jsonify({"message": "Header 'password' not found!"})

    if request.headers["requests-mode"] == "dank":
        sending = dankinforequests
        dankinforequests = []
        return jsonify({"message": "Data sent!", "json": sending})

@app.route("/return-dank-requests", methods=["POST"])
def returndankrequests():
    global dankinforequestsreturn
    try:
        if request.headers["password"] != BOT_AUTH_KEY:
            return jsonify({"message": "Header 'password' incorrect!"})
    except KeyError:
        return jsonify({"message": "Header 'password' not found!"})

    if request.headers["update-mode"] == "dank":
        for datareturn in request.json:
            dankinforequestsreturn[datareturn] = request.json[datareturn]
        return jsonify({"message": "Data accepted!"})

#                 BOT DATA PINGS

@app.route("/update-data", methods=["POST"])
def updatedata():
    try:
        if request.headers["password"] != BOT_AUTH_KEY:
            return jsonify({"message": "Header 'password' incorrect!"})
    except KeyError:
        return jsonify({"message": "Header 'password' not found!"})

    if request.headers["update-mode"] == "server-info":
        with open("data/server-info.json", "w+") as f:
            json.dump(request.json, f)
            f.close()
        return jsonify({"message": "Data accepted!"})

#                 DISCORD 0AUTH2

@app.route('/discord-auth')
def discordauth():
    scope = request.args.get(
        'scope',
        'identify email')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/discord-callback')
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

        return redirect("/")
    except:
        return "500 - Internal Server Error"

@app.route('/discord-signout')
def signout():
    session.clear()
    return redirect("/")

#                 STAIC FILES SERVING

@app.route('/static')
def static_request():
    file = request.args.get('file')
    try:
        return send_file(f'static/{file}', download_name=file)
    except:
        return "File Not Found!", 404


socketio.run(app, debug=True)
