from flask import Flask, redirect, render_template, request, send_file
import glob, ntpath

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/static')
def get_static():
    file = request.args.get('file')
    try:
        return send_file(f'static/{file}', attachment_filename=file)
    except:
        return "File Not Found!", 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
