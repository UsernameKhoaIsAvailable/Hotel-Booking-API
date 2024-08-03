from hotel_booking.app import db


class User(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('guest', 'manager', 'admin'), nullable=False)
