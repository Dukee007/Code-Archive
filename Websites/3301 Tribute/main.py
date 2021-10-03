from flask import Flask, redirect, render_template, request, send_file
import glob, random, os

app = Flask(__name__)

titles = ["3301", "Everywhere"]
songs = ["/file?file=i.mp3", "/file?file=tie.mp3"]

@app.route('/')
def home():
    return render_template("home.html", title=random.choice(titles), song=random.choice(songs))

@app.route('/file')
def file():
    file = request.args.get('file')
    try:
        return send_file(f'files/{file}', attachment_filename=file)
    except:
        return "File Not Found!", 404

@app.route('/static')
def static_request():
    file = request.args.get('file')
    try:
        return send_file(f'static/{file}', attachment_filename=file)
    except:
        return "File Not Found!", 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
