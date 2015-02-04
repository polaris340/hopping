from application import app
from flask import render_template, session
from application.models.schema import Place
from application.models import user_manager

@app.route('/load_comments/<int:place_id>/<int:offset>')
def load_comments(place_id, offset):
    place = Place.query.get(place_id)

    context = {
        'comments':place.load_comments(offset),
        'offset':offset
    }

    if 'user_id' in session:
        context['user'] = user_manager.get_user(session['user_id'])

    return render_template('ajax/comment.html', context = context)