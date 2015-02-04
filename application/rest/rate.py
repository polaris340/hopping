#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify
from application.models.schema import Rate, Place

from json import loads

from lib import login_required




@app.route('/rate/<int:place_id>/<int:value>', methods = ['POST'])
@login_required
def add_rate(place_id, value):

    
    

    if value < 1 or value > 10:
        return jsonify(
            status = 400,
            message = "Rate value must in range 1 to 10"
            ), 400

    try:
        place = Place.query.get(place_id)
        place.add_rate(session['user_id'], value)

        return jsonify(
            status = 200,
            message = "Successfully rated",
            response = place.get_rate_html()
            )
    except:
        
        return jsonify(
            status = 400,
            message = "You already rated this place"
            ), 400

    



@app.route('/rate/<int:place_id>', methods = ['DELETE'])
@login_required
def cancel_rate(place_id):
    place = Place.query.get(place_id)
    try: 
        place.cancel_rate(session['user_id'])

        return jsonify(
            status = 200,
            message = "Successfully removed",
            response = place.get_rate_html()
            )
    except:

        return jsonify(
            status = 404,
            message = "You are not rated this place:" + str(place_id)
            ), 404


    

