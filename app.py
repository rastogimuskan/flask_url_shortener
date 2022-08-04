import json
import os
from werkzeug.utils import  secure_filename

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
app = Flask(__name__)
app.secret_key = "asdfghjklqwertyu"

@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
            if request.form['code'] in urls:
                flash("The give short name is already been used ")
                return redirect(url_for('home'))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('D:/flask_project/first_flask/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}


        with open('urls.json','w') as urls_file:
            json.dump(urls, urls_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as file:
            urls = json.load(file)
            if code in urls:
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                   return redirect(url_for('static', filename='user_files/'+urls[code]['file']))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))