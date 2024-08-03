from datetime import date

from flask_restful import fields, Resource, reqparse, marshal_with

from hotel_booking.models.models import Booking
from hotel_booking.services.booking_services import search_a_service
from hotel_booking.services.modifying_services import add_data
from hotel_booking.services.room_services import search_a_room
from hotel_booking.services.voucher_services import search_a_voucher
from hotel_booking.utils.utils import generate_id

post_parser = reqparse.RequestParser()
post_parser.add_argument('expected_check_in', type=date, location='json', required=True)
post_parser.add_argument('expected_check_out', type=date, location='json', required=True)
post_parser.add_argument('user_id', location='json', required=True)
post_parser.add_argument('room_id', location='json', required=True)
post_parser.add_argument('service_id', location='json', action='append')
post_parser.add_argument('voucher_id', location='json', action='append')
booking_fields = {
    'id': fields.String,
    'expected_check_in': fields.DateTime,
    'expected_check_out': fields.DateTime,
    'check_in': fields.DateTime,
    'check_out': fields.DateTime,
    'base_price': fields.Integer,
    'total_price': fields.Integer,
    'confirmation': fields.String,
    'user_id': fields.String,
    'room_id': fields.String,
}

booking_list_fields = {
    fields.List(fields.Nested(booking_fields))
}


class BookingApi(Resource):
    @marshal_with(booking_fields)
    def post(self):
        args = post_parser.parse_args()
        id = generate_id()
        room = search_a_room(args.room_id)
        base_price = room.price
        total_price = base_price
        if (args.service_id):
            for id in args.service_id:
                service = search_a_service(id)
                base_price += service.price
        discount = 0
        if (args.voucher_id):
            for id in args.voucher_id:
                voucher = search_a_voucher(id)
                discount += voucher.discount
        total_price -= base_price * discount / 100
        booking = Booking(id, args.expected_check_in, args.expected_check_out, base_price, total_price, args.user_id,
                          args.room_id)
        add_data(booking)
        return booking
