from hotel_booking.app import db


class ChosenVoucher(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    voucher_id = db.Column(db.CHAR(50), db.ForeignKey('Voucher.id'))
    booking_id = db.Column(db.CHAR(50), db.ForeignKey('Booking.id'))

    # voucher = db.relationship('Voucher')
    # hotel_booking = db.relationship('Booking')

