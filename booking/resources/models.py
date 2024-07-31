from flask_restful import Resource, fields
from sqlalchemy.orm import Mapped, mapped_column

from booking.app import db

hotel_fields = {
    'id': fields.String,
    'name': fields.String,
    'location': fields.String,
    'district': fields.String,
    'city': fields.String,
    'classification': fields.Integer,
    'description': fields.String,
}
hotel_list_fields = {
    fields.List(fields.Nested(hotel_fields))
}


class Hotel(db.Model, Resource):
    id = db.Column(db.CHAR(50), primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    district = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    classification = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.location = kwargs['location']
        self.district = kwargs['district']
        self.city = kwargs['city']
        self.classification = kwargs['classification']
        self.description = kwargs['description']


class RoomType(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


class User(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('guest', 'manager', 'admin'), nullable=False)


class Room(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    no = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.CHAR(50), db.ForeignKey('RoomType.id'))
    capacity = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))


class HotelManager(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    manager_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # manager = db.relationship('User', backref='Hotel_managers')
    # hotel = db.relationship('Hotel', backref='managers')


class Booking(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    expected_check_in = db.Column(db.Date, nullable=False)
    expected_check_out = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    base_price = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer)
    confirmation = db.Column(db.Enum('pending', 'canceled', 'confirmed', 'refused'))
    user_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))
    room_id = db.Column(db.CHAR(50), db.ForeignKey('Room.id'))

    # user = db.relationship('User', backref='bookings')
    # room = db.relationship('Room', backref='bookings')


class Services(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # hotel = db.relationship('Hotel', backref='services')


class ChosenServices(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    service_id = db.Column(db.CHAR(50), db.ForeignKey('Services.id'))
    booking_id = db.Column(db.CHAR(50), db.ForeignKey('Booking.id'))

    # service = db.relationship('Services')
    # booking = db.relationship('Booking')


class Review(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    star = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String)
    comment = db.Column(db.String)
    user_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))
    room_id = db.Column(db.CHAR(50), db.ForeignKey('Room.id'))

    # user = db.relationship('User', backref='reviews')
    # room = db.relationship('Room', backref='reviews')


class Voucher(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    discount = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('Hotel.id'))

    # hotel = db.relationship('Hotel', backref='vouchers')


class ChosenVoucher(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    voucher_id = db.Column(db.CHAR(50), db.ForeignKey('Voucher.id'))
    booking_id = db.Column(db.CHAR(50), db.ForeignKey('Booking.id'))

    # voucher = db.relationship('Voucher')
    # booking = db.relationship('Booking')


class HotelImage(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    image_path = db.Column(db.String, nullable=False)
    hotel_id = db.Column(db.CHAR(50), db.ForeignKey('hotel.id'))

    # hotel = db.relationship('Hotel', backref='images')


class RoomImage(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    image_path = db.Column(db.String, nullable=False)
    room_id = db.Column(db.CHAR(50), db.ForeignKey('Room.id'))

    # room = db.relationship('Room', backref='images')


class ReviewImage(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    image_path = db.Column(db.String, nullable=False)
    user_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))

    # user = db.relationship('User', backref='review_images')
