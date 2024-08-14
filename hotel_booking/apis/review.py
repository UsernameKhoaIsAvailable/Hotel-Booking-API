from hotel_booking.app import db


class Review(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    star = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String)
    comment = db.Column(db.String)
    user_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))
    room_id = db.Column(db.CHAR(50), db.ForeignKey('Room.id'))

    # user = db.relationship('User', backref='reviews')
    # room = db.relationship('Room', backref='reviews')

