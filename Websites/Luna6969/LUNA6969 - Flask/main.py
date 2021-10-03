from flask import Flask, redirect, render_template, request, send_file
import os, json

app = Flask(__name__)

@app.route('/')
def home():
    with open("database/work.json") as f:
        work = json.load(f)
        f.close()
    return render_template("index.html", work_hours=work["hours"], com_pro=work["projects"], clients=work["clients"], people_love=work["love"])

@app.route('/css', endpoint='css')
@app.route('/js', endpoint='js')
@app.route('/img', endpoint='img')
@app.route('/fonts', endpoint='fonts')
def get_static_file():
    file = request.args.get('file')
    if request.endpoint == "css":
        return send_file(f'static/webfiles/css/{file}', attachment_filename=file)
    elif request.endpoint == "js":
        return send_file(f'static/webfiles/js/{file}', attachment_filename=file)
    elif request.endpoint == "img":
        return send_file(f'static/images/{file}', attachment_filename=file)
    elif request.endpoint == "fonts":
        return send_file(f'static/webfiles/fonts/{file}', attachment_filename=file)

@app.route('/asset-manifest.json')
@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json', attachment_filename="manifest.json")

app.run(port=5000, debug=True)
