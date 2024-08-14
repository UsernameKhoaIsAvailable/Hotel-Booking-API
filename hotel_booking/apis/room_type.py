from hotel_booking.app import db


class RoomType(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
