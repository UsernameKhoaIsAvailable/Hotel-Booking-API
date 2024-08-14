from hotel_booking.app import db


class Voucher(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    discount = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # hotel = db.relationship('Hotel', backref='vouchers')

