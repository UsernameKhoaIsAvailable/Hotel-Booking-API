from hotel_booking.app import db


class HotelManager(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    manager_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # manager = db.relationship('User', backref='Hotel_managers')
    # hotel = db.relationship('Hotel', backref='managers')
