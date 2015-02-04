from schema import Place
from application import db



def get_place(id):
    return Place.query.get(id)


def get_places(start):
    return Place.query.order_by(db.desc(Place.rank)).slice(start, start+8)