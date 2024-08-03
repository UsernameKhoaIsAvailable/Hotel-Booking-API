from hotel_booking.app import db


def add_data(obj):
    db.session.add(obj)
    db.session.commit()


def update_data(obj):
    obj.verified = True
    db.session.commit()


def delete_data(obj):
    db.session.delete(obj)
    db.session.commit()
