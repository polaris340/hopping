from application import app
from flask import request, render_template
from flask_cors import cross_origin
import json

@app.route('/test', methods = ['GET' ,'POST'])
@cross_origin()
def get_post_test():
    if request.method == 'GET':
        return render_template('test.html')
    else:

        response = app.make_response(json.dumps(request.form))
        response.set_cookie("asdfasdfasdf","jkljkljkl")
        response.set_cookie("qerqwer","jkljkljkl")
        return response