from hotel_booking.app import db


class Room(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    no = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.CHAR(50), db.ForeignKey('RoomType.id'))
    capacity = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

