from application import db, app
from schema import User


def add_user(fb_id, email, password, name, fb_updated_time, email_verified, uuid = None):
    user = User(fb_id = fb_id,
        email = email,
        password = db.func.md5(password + app.config['SALT']),
        name = name,
        fb_updated_time = fb_updated_time,
        email_verified = email_verified,
        uuid = uuid)

    db.session.add(user)
    db.session.commit()

    return user

def update_user(id, email, name, fb_updated_time):
    user = User.query.get(id)
    user.email = email
    user.name = name
    user.fb_updated_time = fb_updated_time

    db.session.commit()

def get_user(id):
    return User.query.get(id)

def get_user_by_fb_id(fb_id):
    return User.query.filter(User.fb_id == fb_id).one()

def get_user_by_email(email):
    return User.query.filter(User.email == email)

def verify_email(uuid):
    user = User.query.filter(User.uuid == uuid).one()
    user.email_verified = '1'
    db.session.commit()

def login_check(email, password):
    return User.query.filter(User.email == email, User.password == db.func.md5(password + app.config['SALT'])).count() == 1
