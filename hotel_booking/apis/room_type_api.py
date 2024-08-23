from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, marshal_with, reqparse

from hotel_booking.apis.schemas import room_type_fields, room_type_list_fields
from hotel_booking.models.models import RoomType
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.room_type_services import get_room_type, update_room_type, get_room_types_by_hotel_id
from hotel_booking.utils.utils import generate_id
from hotel_booking.services.hotel_manager_services import check_hotel_manager


class AddAndGetListRoomType(Resource):
    @marshal_with(room_type_fields)
    @jwt_required()
    def post(self, hotel_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json', required=True)
        post_parser.add_argument('description', location='json', required=True)
        manager_id = get_jwt_identity()
        if check_hotel_manager(hotel_id, manager_id):
            args = post_parser.parse_args()
            type_id = generate_id()
            room_type = RoomType(type_id, args.name, args.description, hotel_id)
            add_data(room_type)
            return room_type
        return {'msg': 'This operation is restricted to managers.'}, 403

    @marshal_with(room_type_list_fields)
    def get(self, hotel_id):
        room_types = get_room_types_by_hotel_id(hotel_id)
        return room_types


class UpdateAndDeleteRoomType(Resource):
    @marshal_with(room_type_fields)
    @jwt_required()
    def put(self, room_type_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json')
        post_parser.add_argument('description', location='json')
        room_type = get_room_type(room_type_id)
        manager_id = get_jwt_identity()
        if room_type is None:
            return {'msg': 'Room type not found'}, 404
        elif check_hotel_manager(room_type.hotel_id, manager_id):
            args = post_parser.parse_args()
            room_type = update_room_type(room_type, args)
            return room_type
        return {'msg': ''}, 403

    @jwt_required()
    def delete(self, room_type_id):
        room_type = get_room_type(room_type_id)
        manager_id = get_jwt_identity()
        if room_type is None:
            return {'msg': 'Room type not found'}, 404
        elif check_hotel_manager(room_type.hotel_id, manager_id):
            delete_data(room_type)
            return 200
        return {'msg': ''}, 403
