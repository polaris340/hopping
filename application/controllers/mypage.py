#-*- coding:utf-8 -*-
from application import app
from flask import render_template, request, session, redirect
from auth import decrypt, get_facebook_data


@app.route('/mypage')
def mypage() :
    if 'user_id' not in session:
        if app.config['COOKIE_NAME'] in request.cookies:
            session['facebook_token'] = (decrypt(request.cookies.get(app.config['COOKIE_NAME'])),'')

            try:
                get_facebook_data()
            except:
                pass
        else:
            return redirect(url_for('index'))


    return render_template('index.html');

