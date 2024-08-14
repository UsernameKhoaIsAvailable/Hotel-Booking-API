from hotel_booking.app import db


class RoomImage(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    image_path = db.Column(db.String, nullable=False)
    room_id = db.Column(db.CHAR(50), db.ForeignKey('Room.id'))

    # room = db.relationship('Room', backref='images')

