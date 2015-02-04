#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify
from application.models.schema import CommentLike, Comment

from json import loads

from lib import login_required




@app.route('/comment_like/<int:comment_id>', methods = ['POST'])
@login_required
def add_comment_like(comment_id):

    try:
        comment = Comment.query.get(comment_id)

        if comment.user_id == session['user_id']:
            return jsonify(
                status = 400,
                message = "It's your comment",
                code = 400002,
                response = comment.like_count
                ), 400

        comment.like(session['user_id'])

        return jsonify(
            status = 200,
            message = "Successfully liked",
            response = comment.like_count
            )
    except:
        return jsonify(
            status = 400,
            code = 400001,
            message = "You already liked this comment"
            ), 400

    



@app.route('/comment_like/<int:comment_id>', methods = ['DELETE'])
@login_required
def cancel_comment_like(comment_id):
    try: 
        comment = Comment.query.get(comment_id)
        comment.like_cancel(session['user_id'])

        return jsonify(
            status = 200,
            message = "Successfully removed",
            response = comment.like_count
            )
    except:

        return jsonify(
            status = 404,
            message = "You are not liked this comment:" + str(comment_id)
            ), 404


    

