#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify, render_template
from application.models.schema import PlaceImage, ImageLike
from application.models.schema import User

from lib import login_required


@app.route('/image_like/<int:place_image_id>', methods = ['POST'])
@login_required
def like_image(place_image_id):
    place_image = PlaceImage.query.get(place_image_id)

    try:
        place_image.like(session['user_id'])
        return jsonify(
            status = 200,
            message = 'Successfully liked'
            )
    except:
        return jsonify(
            status = 400,
            message = 'You already liked this image'

            ), 400



