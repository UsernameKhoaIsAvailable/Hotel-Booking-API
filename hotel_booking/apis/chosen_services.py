from hotel_booking.app import db


class ChosenServices(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    service_id = db.Column(db.CHAR(50), db.ForeignKey('Services.id'))
    booking_id = db.Column(db.CHAR(50), db.ForeignKey('Booking.id'))

    # service = db.relationship('Services')
    # hotel_booking = db.relationship('Booking')

