from flask import Flask, redirect, render_template, request
import glob, ntpath

app = Flask(__name__)

users = {
"luna": "Infocushd$25",
"redd": "reddlol90",
}

authed = {}

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    authed[str(request.remote_addr)] = False
    if request.method == "GET":
        return render_template("login.html", msg=None)
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in users:
            if password == users[username]:
                authed[str(request.remote_addr)] = True
                return redirect("/dashboard")
        elif username == "" or password == "":
            return render_template("login.html", msg="You cannot leave an input blank!")
        else:
            return render_template("login.html", msg="Wrong Password or Username!")


@app.route('/dashboard')
def dashboard():
    try:
        if authed[str(request.remote_addr)]:
            data = {}
            for file in glob.glob("data/*.*"):
                filename = ntpath.basename(file)
                f = open(file)
                data[filename] = str(f.read())
                f.close()
            ht = data["home-link-twitch.clicks"]
            htw = data["home-link-twitter.clicks"]
            hy = data["home-link-youtube.clicks"]
            st = data["sub-link-twitch.clicks"]
            stw = data["sub-link-twitter.clicks"]
            sy = data["sub-link-youtube.clicks"]
            return render_template("dashboard.html", ht=ht, htw=htw, hy=hy, st=st, stw=stw, sy=sy)
        else:
            authed[str(request.remote_addr)] = False
            return redirect("/login")
    except Exception as e:
        authed[str(request.remote_addr)] = False
        return redirect("/login")

@app.route('/utmredirect/')
def redirecttosite():
    camp = request.args.get('utm-campaign')
    site = request.args.get('utm-site')
    if camp == "home-link":
        f = open(f"data/home-link-{site}.clicks")
        towrite = int(f.read()) + 1
        f.close()
        f = open(f"data/home-link-{site}.clicks", "w+")
        f.write(str(towrite))
        f.close()
    elif camp == "sub-link":
        f = open(f"data/sub-link-{site}.clicks")
        towrite = int(f.read()) + 1
        f.close()
        f = open(f"data/sub-link-{site}.clicks", "w+")
        f.write(str(towrite))
        f.close()

    if site == "twitch":
        return redirect("https://www.twitch.tv/redd60")
    elif site == "twitter":
        return redirect("https://twitter.com/ReddTTV")
    elif site == "youtube":
        return redirect("https://www.youtube.com/channel/UC3TA76lEX-gCJJPzLk-DWCQ")
    else:
        return "404 - Page Not Found!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
