from datetime import date

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import fields, Resource, reqparse, marshal_with

from hotel_booking.apis.schemas import booking_fields
from hotel_booking.models.models import Booking
from hotel_booking.services.booking_services import get_booking, search_chosen_services, search_chosen_vouchers, \
    update_booking
from hotel_booking.services.modifying_services import add_data, update_data
from hotel_booking.services.room_services import get_room
from hotel_booking.utils.utils import generate_id, calculate_base_price, calculate_total_price, \
    convert_string_to_date, subtract_2_date, check_hotel_manager_by_room_id

post_parser = reqparse.RequestParser()

booking_list_fields = {
    fields.List(fields.Nested(booking_fields))
}


class CreateBooking(Resource):
    @marshal_with(booking_fields)
    @jwt_required()
    def post(self):
        post_parser.add_argument('expected_check_in', type=date, location='json', required=True)
        post_parser.add_argument('expected_check_out', type=date, location='json', required=True)
        post_parser.add_argument('room_id', location='json', required=True)
        post_parser.add_argument('service_ids', location='json', action='append')
        post_parser.add_argument('voucher_ids', location='json', action='append')
        args = post_parser.parse_args()
        booking_id = generate_id()
        room = get_room(args.room_id)
        expected_check_in = convert_string_to_date(args.expected_check_in)
        expected_check_out = convert_string_to_date(args.expected_check_out)
        base_price = room.price * subtract_2_date(expected_check_in, expected_check_out)
        user_id = get_jwt_identity()
        base_price = calculate_base_price(args.service_ids, booking_id, base_price)
        total_price = calculate_total_price(args.voucher_ids, booking_id, base_price)
        booking = Booking(booking_id, expected_check_in, expected_check_out, base_price, total_price, user_id,
                          args.room_id)
        add_data(booking)
        booking = get_booking(booking_id)
        chosen_services = search_chosen_services(booking_id)
        chosen_vouchers = search_chosen_vouchers(booking_id)
        return booking, room, chosen_services, chosen_vouchers


class UpdateBooking(Resource):
    @marshal_with(booking_fields)
    @jwt_required()
    def put(self, booking_id):
        post_parser.add_argument('expected_check_in', type=date, location='json')
        post_parser.add_argument('expected_check_out', type=date, location='json')
        post_parser.add_argument('room_id', location='json')
        post_parser.add_argument('service_ids', location='json', action='append')
        post_parser.add_argument('voucher_ids', location='json', action='append')
        user_id = get_jwt_identity()
        booking = get_booking(booking_id)
        if user_id != booking.user_id:
            return {'msg': 'This booking does not belong to current user.'}, 403
        args = post_parser.parse_args()
        booking = update_booking(booking, args)
        return booking


class ConfirmBooking(Resource):
    @marshal_with(booking_fields)
    @jwt_required()
    def put(self, booking_id):
        post_parser.add_argument('confirmation', location='json')
        booking = get_booking(booking_id)
        claims = get_jwt()
        if booking.confirmation != 'refused' and booking.confirmation != 'canceled':
            if claims['role'] == 'user':
                user_id = get_jwt_identity()
                if user_id == booking.user_id:
                    booking.confirmation = 'canceled'
                    update_data(booking)
                    return booking
                return {'msg': 'This booking does not belong to current user.'}, 403
            elif claims['role'] == 'manager':
                manager_id = get_jwt_identity()
                if check_hotel_manager_by_room_id(booking.room_id, manager_id):
                    args = post_parser.parse_args()
                    booking.confirmation = args.confirmation
                    update_data(booking)
                    return booking
                return {'msg': 'This booking is not under your management.'}, 403
        return {'msg': ''}
