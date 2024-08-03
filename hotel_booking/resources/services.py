from hotel_booking.app import db


class Services(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # hotel = db.relationship('Hotel', backref='services')


