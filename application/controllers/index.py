#-*- coding:utf-8 -*-
from application import app
from flask import render_template, request, session
from auth import decrypt, get_facebook_data


@app.route('/')
@app.route('/index')
def index() :
    if 'user_id' not in session and app.config['COOKIE_NAME'] in request.cookies:
        session['facebook_token'] = (decrypt(request.cookies.get(app.config['COOKIE_NAME'])),'')

        try:
            get_facebook_data()
        except:
            pass


    return render_template('index.html');



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
