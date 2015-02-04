#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify, render_template
from application.models.schema import Comment
from application.controllers.place import get_place_detail
from json import loads

from lib import login_required



@app.route('/comment/<int:place_id>', methods = ['POST'])
@login_required
def add_comment(place_id):

    comment = Comment(
        user_id = session['user_id'],
        place_id = place_id
        )
    
    # update using json body
    print loads(request.data)
    try:
        data = loads(request.data)
        for c in data:
            setattr(comment, c, data[c])
    except:
        pass

    if not comment.body:
        return jsonify(
            status = 400,
            message = "Comment body required"
            ), 400

    db.session.add(comment)
    db.session.commit()



    return jsonify(
        status = 200,
        message = "Successfully commented",
        response = render_template('ajax/best_comment.html', comment = comment)
        )

@app.route('/comment/<int:comment_id>', methods = ['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    place_id = comment.place_id
    if comment.user_id != session['user_id']:
        return jsonify(
            status = 401,
            message = "It's not your comment"
            ), 401
    comment.likes.delete()
    db.session.delete(comment)
    db.session.commit()

    return jsonify(
        status = 200,
        message = "Successfully deleted",
        response = get_place_detail(place_id)
        )

