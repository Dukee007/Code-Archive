from flask import Flask, redirect, render_template, request, url_for, g, session, jsonify
import json, os

app = Flask(__name__)

API_ACCESS_CODE = "*Y*&£G**BBIBUIYG(*&^TG*(Y675y0(UH$&*GBt976r6"

#                 MAIN PAGES

@app.route('/')
def home():
    return "Hey dumb bitch what the hell are you doing here goto the <a href='/docs/?page=intro'>api docs</a> to learn how to use this!"

@app.route('/docs/')
def docs():
    page = request.args.get('page')
    if page == None:
        return render_template("docs.html", intro=False)
    else:
        return render_template("docs.html", intro=True)

@app.route('/botupdate/', methods=["POST", "GET"])
def server():
    if request.method == "GET":
        code = request.headers.get('authorization')
        api_request = request.headers.get('api_request')
        bot = request.headers.get('bot')

        if code != API_ACCESS_CODE:
            return jsonify({"401": "Authorization Incorrect"}), 401

        elif bot not in ["tbdb", "wealthy", "nsfw", "beats"]:
            return jsonify({"404": "Bot Not Found"}), 404

        if api_request == "premium_servers":
            f = open(f"premium/servers/{bot}.json")
            return jsonify(json.load(f))

        elif api_request == "premium_users":
            f = open(f"premium/users/{bot}.json")
            return jsonify(json.load(f))


    elif request.method == "POST":
        code = request.headers.get('authorization')
        api_request = request.headers.get('api_request')
        bot = request.headers.get('bot')

        if code != API_ACCESS_CODE:
            return jsonify({"401": "Authorization Incorrect"}), 401

        elif bot not in ["tbdb", "wealthy", "nsfw", "beats"]:
            return jsonify({"404": "Bot Not Found"}), 404

        if api_request == "add_premium_server":
            id = request.headers.get('guild_id')
            f = open(f"premium/servers/{bot}.json")
            premium_servers = json.load(f)
            f.close()
            premium_servers.append(str(id))
            f = open(f"premium/servers/{bot}.json", "w+")
            json.dump(premium_servers, f)
            f.close()
            return jsonify({"200": f"Guild {str(id)} Added"})

        if api_request == "remove_premium_server":
            id = request.headers.get('guild_id')
            f = open(f"premium/servers/{bot}.json")
            premium_servers = json.load(f)
            f.close()
            premium_servers.remove(str(id))
            f = open(f"premium/servers/{bot}.json", "w+")
            json.dump(premium_servers, f)
            f.close()
            return jsonify({"200": f"Guild {str(id)} Removed"})

        if api_request == "add_premium_user":
            id = request.headers.get('user_id')
            f = open(f"premium/users/{bot}.json")
            premium_users = json.load(f)
            f.close()
            premium_users.append(str(id))
            f = open(f"premium/users/{bot}.json", "w+")
            json.dump(premium_users, f)
            f.close()
            return jsonify({"200": f"User {str(id)} Added"})

        if api_request == "remove_premium_user":
            id = request.headers.get('user_id')
            f = open(f"premium/users/{bot}.json")
            premium_users = json.load(f)
            f.close()
            premium_users.remove(str(id))
            f = open(f"premium/users/{bot}.json", "w+")
            json.dump(premium_users, f)
            f.close()
            return jsonify({"200": f"User {str(id)} Removed"})






app.run(port=5000, debug=True)
