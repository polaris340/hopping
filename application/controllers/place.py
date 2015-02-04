from flask import render_template, session
from application import app
from application.models import place_manager, user_manager



@app.route('/get_places/<int:start>')
def get_places(start):
    places = place_manager.get_places(start)

    context = {
        'places':places
        
    }

    if 'user_id' in session:
        context['user'] = user_manager.get_user(session['user_id'])

    return render_template('ajax/card.html', context = context)

@app.route('/get_place_detail/<int:id>')
def get_place_detail(id):
    place = place_manager.get_place(id)

    context = {
        'place':place
    }


    comment_context = {
        'comments':place.get_top_comments(),
        'offset':0
    }


    if 'user_id' in session:
        context['user'] = user_manager.get_user(session['user_id'])
        comment_context['user'] = context['user']

    


    context['comment_html'] = render_template('ajax/comment.html', context = comment_context)

    return render_template('ajax/modal_content.html', context = context)

