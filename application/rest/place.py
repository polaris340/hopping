#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify, render_template
from application.models.schema import Place
from application.models.schema import User

from lib import login_required
from json import loads

@app.route('/place/<int:offset>/<int:limit>', methods = ["GET"])
def get_place_card_list(offset, limit):
    
    if request.referrer.split('/')[-1] == 'mypage' and 'user_id' in session:
        data = Place.get_card_data_list(offset, limit, session['user_id'], True)
    else:
        if 'user_id' in session:
            data = Place.get_card_data_list(offset, limit, session['user_id'])
        else:
            data = Place.get_card_data_list(offset, limit)

    return jsonify(
        status = 200,
        message = "Successfully loaded",
        data = data
        )

@app.route('/place/search/<keyword>', methods = ['GET'])
def place_search(keyword):

    offset = 0
    limit = 12

    if request.referrer.split('/')[-1] == 'mypage' and 'user_id' in session:
        data = Place.get_card_data_list(offset, limit, session['user_id'], True, keyword)
    else:
        if 'user_id' in session:
            data = Place.get_card_data_list(offset, limit, session['user_id'], False, keyword)
        else:
            data = Place.get_card_data_list(offset, limit, None, False, keyword)

    return jsonify(
        status = 200,
        message = "Successfully loaded",
        data = data
        )



@app.route('/place/<int:place_id>', methods = ['GET'])
def get_place_card(place_id):
    place = Place.query.get(place_id)

    if 'user_id' in session:
        data = place.get_card_data(session['user_id'])
    else:
        data = place.get_card_data()

    return jsonify(
        status = 200,
        message = "Successfully loaded",
        data = data
        )

    # context = {
    #     'places':[place]
    # }

    # if 'user_id' in session:
    #     context['user'] = User.query.get(session['user_id'])

    # return jsonify(
    #     status = 200,
    #     message = "Successfully loaded",
    #     response = render_template('ajax/card.html', context = context)

    #     )