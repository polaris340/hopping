from flask import session, jsonify
from functools import wraps


def login_required(func):

    @wraps(func)
    def login_check(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(
                status = 401,
                message = "Not logged in"
            ), 401
        else:
            return func(*args, **kwargs)

    return login_check