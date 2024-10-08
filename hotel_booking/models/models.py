from hotel_booking.app import db


class Hotel(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    classification = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, id, name, address, district, city, classification, description):
        self.id = id
        self.name = name
        self.address = address
        self.district = district
        self.city = city
        self.classification = classification
        self.description = description


class RoomType(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    def __init__(self, id, name, description, hotel_id):
        self.id = id
        self.name = name
        self.description = description
        self.hotel_id = hotel_id


class User(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('guest', 'manager', 'admin'), nullable=False)
    token = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean)

    def __init__(self, id, first_name, last_name, email, password, role, token):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.token = token
        self.is_verified = False


class Room(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    no = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.CHAR(20), db.ForeignKey('room_type.id'))
    capacity = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    def __init__(self, id, no, price, type_id, capacity, hotel_id):
        self.id = id
        self.no = no
        self.price = price
        self.type_id = type_id
        self.capacity = capacity
        self.hotel_id = hotel_id


class HotelManager(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    manager_id = db.Column(db.CHAR(20), db.ForeignKey('user.id'))
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    # manager = db.relationship('User', backref='Hotel_managers')
    # hotel = db.relationship('Hotel', backref='managers')
    def __init__(self, id, manager_id, hotel_id):
        self.id = id
        self.manager_id = manager_id
        self.hotel_id = hotel_id


class Booking(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    expected_check_in = db.Column(db.Date, nullable=False)
    expected_check_out = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    base_price = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer)
    confirmation = db.Column(db.Enum('pending', 'canceled', 'confirmed', 'refused'))
    user_id = db.Column(db.CHAR(20), db.ForeignKey('user.id'))
    room_id = db.Column(db.CHAR(20), db.ForeignKey('room.id'))

    # user = db.relationship('User', backref='bookings')
    # room = db.relationship('Room', backref='bookings')
    def __init__(self, id, expected_check_in, expected_check_out, base_price, total_price, user_id,
                 room_id):
        self.id = id
        self.expected_check_in = expected_check_in
        self.expected_check_out = expected_check_out
        self.base_price = base_price
        self.total_price = total_price
        self.confirmation = 'pending'
        self.user_id = user_id
        self.room_id = room_id


class Services(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    # hotel = db.relationship('Hotel', backref='services')
    def __init__(self, id, name, description, price, hotel_id):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.hotel_id = hotel_id


class ChosenServices(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    service_id = db.Column(db.CHAR(20), db.ForeignKey('services.id'))
    booking_id = db.Column(db.CHAR(20), db.ForeignKey('booking.id'))

    # service = db.relationship('Services')
    # booking = db.relationship('Booking')
    def __init__(self, id, service_id, booking_id):
        self.id = id
        self.service_id = service_id
        self.booking_id = booking_id


class Review(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    star = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    user_id = db.Column(db.CHAR(20), db.ForeignKey('user.id'))
    room_id = db.Column(db.CHAR(20), db.ForeignKey('room.id'))

    # user = db.relationship('User', backref='reviews')
    # room = db.relationship('Room', backref='reviews')

    def __init__(self, id, star, title, comment, user_id, room_id):
        self.id = id
        self.star = star
        self.title = title
        self.comment = comment
        self.user_id = user_id
        self.room_id = room_id


class Voucher(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    # hotel = db.relationship('Hotel', backref='vouchers')
    def __init__(self, id, name, discount, hotel_id):
        self.id = id
        self.name = name
        self.discount = discount
        self.hotel_id = hotel_id


class ChosenVoucher(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    voucher_id = db.Column(db.CHAR(20), db.ForeignKey('voucher.id'))
    booking_id = db.Column(db.CHAR(20), db.ForeignKey('booking.id'))

    # voucher = db.relationship('Voucher')
    # booking = db.relationship('Booking')
    def __init__(self, id, voucher_id, booking_id):
        self.id = id
        self.voucher_id = voucher_id
        self.booking_id = booking_id


class HotelImage(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    hotel_id = db.Column(db.CHAR(20), db.ForeignKey('hotel.id'))

    # hotel = db.relationship('Hotel', backref='images')
    def __init__(self, id, image_path, hotel_id):
        self.id = id
        self.image_path = image_path
        self.hotel_id = hotel_id


class RoomImage(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.CHAR(20), db.ForeignKey('room.id'))

    # room = db.relationship('Room', backref='images')
    def __init__(self, id, image_path, room_id):
        self.id = id
        self.image_path = image_path
        self.room_id = room_id


class ReviewImage(db.Model):
    id = db.Column(db.CHAR(20), primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    review_id = db.Column(db.CHAR(20), db.ForeignKey('review.id'))

    # user = db.relationship('User', backref='review_images')
    def __init__(self, id, image_path, review_id):
        self.id = id
        self.image_path = image_path
        self.review_id = review_id
