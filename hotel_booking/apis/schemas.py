from flask_restful import fields

user_fields = {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'role': fields.String,
}

room_image_fields = {
    'image_path': fields.String,
}

room_type_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
}

room_fields = {
    'id': fields.String,
    'no': fields.Integer,
    'price': fields.Integer,
    'capacity': fields.Integer,
    'type': fields.Nested(room_type_fields),
    'images': fields.List(fields.Nested(room_image_fields)),
}

hotel_image_fields = {
    'image path': fields.String,
}

hotel_fields = {
    'id': fields.String,
    'name': fields.String,
    'address': fields.String,
    'district': fields.String,
    'city': fields.String,
    'classification': fields.Integer,
    'description': fields.String,
    'images': fields.List(fields.Nested(hotel_image_fields)),
}

voucher_fields = {
    'id': fields.String,
    'discount': fields.Integer,
}

service_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Integer,
}

booking_fields = {
    'id': fields.String,
    'expected_check_in': fields.DateTime,
    'expected_check_out': fields.DateTime,
    'check_in': fields.DateTime,
    'check_out': fields.DateTime,
    'base_price': fields.Integer,
    'total_price': fields.Integer,
    'confirmation': fields.String,
    'room': fields.Nested(room_fields),
    'services': fields.List(fields.Nested(service_fields)),
    'vouchers': fields.List(fields.Nested(voucher_fields)),
}

review_image_fields = {
    'id': fields.String,
    'image_path': fields.String,
}

review_fields = {
    'id': fields.String,
    'star': fields.Integer,
    'title': fields.String,
    'comment': fields.String,
    'images': fields.List(fields.Nested(review_image_fields)),
}

user_list_fields = {
    'users': fields.List(fields.Nested(user_fields))
}

hotel_list_fields = {
    'hotels': fields.List(fields.Nested(hotel_fields))
}

booking_list_fields = {
    'bookings': fields.List(fields.Nested(booking_fields))
}

room_list_fields = {
    'rooms': fields.List(fields.Nested(room_fields))
}

room_type_list_fields = {
    'room_types': fields.List(fields.Nested(room_type_fields))
}

service_list_fields = {
    'services': fields.List(fields.Nested(service_fields))
}

voucher_list_fields = {
    'vouchers': fields.List(fields.Nested(voucher_fields))
}

review_list_fields = {
    'reviews': fields.List(fields.Nested(review_fields))
}