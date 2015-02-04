#-*- coding: utf-8 -*-
from application import app, oauth, facebook, aes

from flask import url_for, request, session, redirect, render_template, flash
from base64 import b64encode, b64decode
from application.models import user_manager
from datetime import datetime, timedelta
from uuid import uuid4
from re import match
from google.appengine.api import mail
from base64 import b64encode, b64decode

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('user_id', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or url_for('index'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    

    session['facebook_token'] = (resp['access_token'], '')
    try:
        get_facebook_data()   
        redirect_to = redirect(next_url)
        response = app.make_response(redirect_to)  
        expire_date = datetime.now() + timedelta(days = 30)
        response.set_cookie(app.config['COOKIE_NAME'],value=encrypt(resp['access_token']), expires = expire_date)     
        return response
    except:
        # 로그인 실패 
        return redirect(url_for('index'))


# hopp 계정 로그인 / 가입
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login_submit', methods = ['POST'])
def login_submit():
    email = request.form['input-email']
    password = request.form['input-password']
    
    if not user_manager.login_check(email, password):
        flash(u'로그인에 실패하였습니다. 이메일과 비밀번호를 확인해주세요')
        return redirect(url_for('login'))
    user = user_manager.get_user_by_email(email).one()
    if not user.email_verified:
        flash(u'메일 인증을 완료해주세요')
        return redirect(url_for('login'))
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route('/email_check', methods = ['POST'])
def email_duplicate_check():
    email = request.form['email']
    if user_manager.get_user_by_email(email).count() > 0:
        return 'email duplicated',400

    return '0'

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup_submit', methods = ['POST'])
def signup_submit():
    email_pattern = '^([0-9a-zA-Z_]([-._\\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\\w]*[0-9a-zA-Z]\\.)+[a-zA-Z]{2,9})$'
    if not match(email_pattern, request.form['input-email']):
        flash(u'이메일 형식이 올바르지 않습니다')
        return redirect(url_for('signup'))

    if user_manager.get_user_by_email(request.form['input-email']).count() > 0:
        flash(u'사용중인 이메일입니다')
        return redirect(url_for('signup'))

    if not (6 <= len(request.form['input-password']) <= 20):
        flash(u'비밀번호는 6~20자로 입력해주세요')
        return redirect(url_for('signup'))
    if (request.form['input-password'] != request.form['input-password-confirm']):
        flash(u'비밀번호가 일치하지 않습니다')
        return redirect(url_for('signup'))



    uuid = str(uuid4())
    user = user_manager.add_user(
            None,
            request.form['input-email'],
            request.form['input-password'],
            request.form['input-name'],
            None,
            '0',
            uuid
            )

    verify_url = "http://"+request.headers.get('Host')+"/verify/"+uuid

    mail.send_mail(sender="HOPP <hopping14@gmail.com>",
              to=request.form['input-email'],
              subject=u"HOPP 메일 인증",
              html=u'''아래 링크를 클릭해주세요.<br>
              <a href="'''+verify_url+u'''">HOPP 메일 인증</a>
            ''',
            body=u'''HOPP 메일 인증 : '''+verify_url)

    flash(u'가입되었습니다. 메일을 확인해주세요')
    return redirect(url_for('login'))

@app.route('/verify/<uuid>')
def verify_email(uuid):
    try:
        user_manager.verify_email(uuid)
        flash(u'메일이 인증되었습니다.')
        return redirect(url_for('login'))
    except:
        return 'Page not found',404

@app.route("/logout")
def logout():
    pop_login_session()
    response = app.make_response(redirect(url_for('index')))
    response.set_cookie(app.config['COOKIE_NAME'],'',expires = 0)
    return response



def get_facebook_data():
    data = facebook.get('/me').data
    try:
        user = user_manager.get_user_by_fb_id(data['id'])
        if user.fb_updated_time != data['updated_time']:
            user_manager.update_user(user.id, data['email'], data['name'], data['updated_time'])
    except:
        user = user_manager.add_user(
            data['id'],
            data['email'],
            None,
            data['name'],
            data['updated_time'],
            '1'
            )

    session['user_id'] = user.id





# AES encrypt and decrypt
def pad(s):
    return s + (aes.block_size - len(s) % aes.block_size) * app.config['AES_PAD']


def encrypt(s):
    return b64encode(aes.encrypt(pad(s)))

def decrypt(s):
    return aes.decrypt(b64decode(s)).rstrip(app.config['AES_PAD'])



