import json
import os
import glob
import re

from flask import Flask, redirect, render_template, request, session, jsonify
from requests_oauthlib import OAuth2Session

POST_KEY = "v&%^TUD796tgyRE(%&^FGv68R6p8f97%RTGd6fg8rOF*)*Fo7do7tD*O"

OAUTH2_CLIENT_ID = "788862752721731654"
OAUTH2_CLIENT_SECRET = 'qRm0_obc23qQ9jDVmQVOL_MQ8tLIPWll'
OAUTH2_REDIRECT_URI = 'http://localhost:5000/discord-callback'  # https://lunabots.xyz/discord-callback

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

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


@app.route('/')
def home():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()

    try:
        if user["message"] == "401: Unauthorized":
            return redirect("/discord-auth")

        pfp = "https://lunabots.xyz/static/assets/discord-server-icon.jpg"
        name = "Error"
        discrim = "Error"
    except KeyError:
        if "a_" in user["avatar"]:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.gif"
        else:
            pfp = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        name = user["username"]
        discrim = user["discriminator"]

    num = 0
    ogguilds = guilds
    guilds = []

    for guild in ogguilds:
        if (guild["permissions"] & 0x128) == 0x128:
            guilds.append(guild)
        num += 1

    num = 0

    for guild in guilds:
        try:
            if "a_" in guild["icon"]:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.gif'
            else:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.jpg'
        except TypeError:
            guilds[num]["icon_url"] = "https://lunabots.xyz/static/assets/discord-server-icon.jpg"
        num += 1

    num = 0

    for guild in guilds:
        try:
            guilds[num]["bot_invite"] = 'https://discord.com/api/oauth2/authorize?client_id=788862752721731654&permissions=8&scope=bot&guild_id=' + guilds[num]["id"]
        except KeyError:
            pass
        num += 1

    guildsin = []

    for server in glob.glob("data/guild/*.json"):
        server = re.sub("[^0-9]", "", server)
        guildsin.append(server)


    return render_template("home.html", pfp=pfp, name=name, discrim=discrim, guilds=guilds, guildsin=guildsin)


@app.route('/<guild_id>')
def logs_home(guild_id):
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()

    try:
        if user["message"] == "401: Unauthorized":
            return redirect("/discord-auth")
    except KeyError:
        pass

    num = 0
    ogguilds = guilds
    guilds = []

    for guild in ogguilds:
        if (guild["permissions"] & 0x128) == 0x128:
            guilds.append(guild)
        num += 1

    num = 0

    for guild in guilds:
        try:
            if "a_" in guild["icon"]:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.gif'
            else:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.jpg'
        except TypeError:
            guilds[num]["icon_url"] = "https://lunabots.xyz/static/assets/discord-server-icon.jpg"
        num += 1

    try:
        guild_id = int(guild_id)
        guild_id = str(guild_id)
    except ValueError:
        return render_template("404.html"), 404
    try:
        f = open(f"data/guild/{str(guild_id)}.json")
        data = json.load(f)
        f.close()
        name = data["name"]
        avatar = data["avatar"]
        f = open(f"data/logs/{str(guild_id)}.json")
        logs = json.load(f)
    except FileNotFoundError:
        return render_template("404_GUILD.html"), 404

    allowed = False

    for guild in guilds:
        if str(guild["id"]) == str(guild_id):
            allowed = True

    if not allowed:
        return render_template("401_GUILD.html"), 401

    if avatar == "":
        avatar = "https://lunabots.xyz/static/assets/discord-server-icon.jpg"

    msgs_sent = str(len(logs["message"]))
    msgs = []

    for x in logs["message"]:
        msgs.append(len(x["content"]))

    try:
        ave_msg_len = round(sum(msgs) / len(msgs))
    except ZeroDivisionError:
        ave_msg_len = "N/A"

    return render_template("serverhome.html", guild_id=guild_id, name=name, avatar=avatar, msgs_sent=msgs_sent,
                           ave_msg_len=ave_msg_len)


@app.route('/<guild_id>/<page>')
def logs_pages(guild_id, page):
    try:
        guild_id = int(guild_id)
        guild_id = str(guild_id)
    except ValueError:
        return render_template("404.html"), 404
    try:
        f = open(f"data/logs/{str(guild_id)}.json")
        logs = json.load(f)
    except FileNotFoundError:
        return render_template("404_GUILD.html"), 404

    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()

    try:
        if user["message"] == "401: Unauthorized":
            return redirect("/discord-auth")
    except KeyError:
        pass

    num = 0
    ogguilds = guilds
    guilds = []

    for guild in ogguilds:
        if (guild["permissions"] & 0x128) == 0x128:
            guilds.append(guild)
        num += 1

    num = 0

    for guild in guilds:
        try:
            if "a_" in guild["icon"]:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.gif'
            else:
                guilds[num]["icon_url"] = 'https://cdn.discordapp.com/icons/' + guild['id'] + '/' + guild[
                    'icon'] + '.jpg'
        except TypeError:
            guilds[num]["icon_url"] = "https://lunabots.xyz/static/assets/discord-server-icon.jpg"
        num += 1

    try:
        guild_id = int(guild_id)
        guild_id = str(guild_id)
    except ValueError:
        return render_template("404.html"), 404
    try:
        f = open(f"data/guild/{str(guild_id)}.json")
        data = json.load(f)
        f.close()
        name = data["name"]
        avatar = data["avatar"]
        f = open(f"data/logs/{str(guild_id)}.json")
        logs = json.load(f)
    except FileNotFoundError:
        return render_template("404_GUILD.html"), 404

    allowed = False

    for guild in guilds:
        if str(guild["id"]) == str(guild_id):
            allowed = True

    if not allowed:
        return render_template("401_GUILD.html"), 401

    if page == "members":
        return render_template("members.html", logs=logs, guild_id=guild_id)

    elif page == "messages":
        logs = logs["message"]
        return render_template("messages.html", logs=logs, guild_id=guild_id)

    elif page == "server":
        return render_template("server.html", logs=logs, guild_id=guild_id)

    else:
        return "Page Not Found!"


@app.route("/post", methods=["POST"])
def post():
    if request.headers.get('auth') != POST_KEY:
        return jsonify({"message": "401 - Invalid Auth"}), 401

    reason = request.headers.get('reason')

    if reason == "data_update":
        data = request.get_json()
        for guild in data:
            guild = str(guild)
            messagedata = data[guild]["message"]
            memberdata = data[guild]["member"]
            serverdata = data[guild]["server"]

            try:
                with open(f"data/guild/{guild}.json") as f:
                    f.close()
            except FileNotFoundError:
                return jsonify({"message": "404 - Guild Not Found"}), 404

            with open(f"data/logs/{guild}.json") as f:
                old_data = json.load(f)
                f.close()

            for message in messagedata:
                old_data["message"].insert(0, message)

            for member in memberdata:
                old_data["member"].insert(0, member)

            for server in serverdata:
                old_data["server"].insert(0, server)

            with open(f"data/logs/{guild}.json", "w+") as f:
                json.dump(old_data, f)
                f.close()

        return jsonify({"message": "200 - Data Accepted"}), 200

    elif reason == "add_guild":
        guild_id = request.headers.get('id')
        try:
            with open(f"data/guild/{guild_id}.json") as f:
                f.close()
            return jsonify({"message": "409 - Guild Already Added"}), 409
        except FileNotFoundError:
            guild_name = request.headers.get('name')
            guild_avatar = request.headers.get('avatar')
            guild_channels = request.get_json()

            with open(f"data/guild/{guild_id}.json", "w+") as f:
                json.dump({"id": str(guild_id), "name": guild_name, "avatar": guild_avatar, "channels": guild_channels}, f)
                f.close()

            with open(f"data/logs/{guild_id}.json", "w+") as f:
                json.dump({"message": [], "member": [], "server": []}, f)
                f.close()

            return jsonify({"message": "200 - Guild Added"}), 200

    elif reason == "remove_guild":
        guild_id = request.headers.get('id')
        try:
            with open(f"data/guild/{guild_id}.json") as f:
                f.close()
            with open(f"data/logs/{guild_id}.json") as f:
                f.close()

            os.remove(f"data/logs/{guild_id}.json")
            os.remove(f"data/guild/{guild_id}.json")

            return jsonify({"message": "200 - Guild Removed"}), 200
        except FileNotFoundError:
            return jsonify({"message": "404 - Guild Not Found"}), 404

    else:
        return jsonify({"message": "404 - Reason Not Found"}), 404


@app.route('/discord-auth')
def discordauth():
    scope = request.args.get(
        'scope',
        'identify guilds')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/discord-signout')
def signout():
    session.clear()
    return redirect("/")


@app.route('/discord-callback')
def callback():
    # noinspection PyBroadException
    try:
        if request.values.get('error'):
            return request.values['error']
        discord = make_session(state=session.get('oauth2_state'))
        token = discord.fetch_token(
            TOKEN_URL,
            client_secret=OAUTH2_CLIENT_SECRET,
            authorization_response=request.url)
        session['oauth2_token'] = token

        return redirect("/")

    except:
        return redirect("/discord-auth")


app.run(port=5000, debug=True)
