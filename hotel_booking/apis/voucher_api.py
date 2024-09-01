from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource, marshal_with

from hotel_booking.apis.schemas import voucher_fields, voucher_list_fields
from hotel_booking.models.models import Voucher
from hotel_booking.services.hotel_manager_services import check_hotel_manager
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.voucher_services import get_vouchers_by_hotel_id, get_voucher, update_voucher
from hotel_booking.utils.utils import generate_id


class AddAndGetListVoucher(Resource):
    @marshal_with(voucher_fields)
    @jwt_required()
    def post(self, hotel_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json', required=True)
        post_parser.add_argument('discount', type=int, location='json', required=True)
        manager_id = get_jwt_identity()
        if check_hotel_manager(hotel_id, manager_id):
            args = post_parser.parse_args()
            voucher_id = generate_id()
            voucher = Voucher(voucher_id, args.name, args.discount, hotel_id)
            add_data(voucher)
            return voucher
        return {'msg': 'This operation is restricted to managers.'}, 403

    @marshal_with(voucher_list_fields)
    def get(self, hotel_id):
        vouchers = get_vouchers_by_hotel_id(hotel_id)
        return {'vouchers': vouchers}


class UpdateAndDeleteVoucher(Resource):
    @marshal_with(voucher_fields)
    @jwt_required()
    def put(self, voucher_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json')
        post_parser.add_argument('discount', type=int, location='json')
        voucher = get_voucher(voucher_id)
        manager_id = get_jwt_identity()
        if check_hotel_manager(voucher.hotel_id, manager_id):
            args = post_parser.parse_args()
            voucher = update_voucher(voucher, args)
            return voucher
        return {'msg': 'This operation is restricted to managers.'}, 403

    @jwt_required()
    def delete(self, voucher_id):
        voucher = get_voucher(voucher_id)
        manager_id = get_jwt_identity()
        if check_hotel_manager(voucher.hotel_id, manager_id):
            delete_data(voucher)
            return 200
        return {'msg': 'This operation is restricted to managers.'}, 403
