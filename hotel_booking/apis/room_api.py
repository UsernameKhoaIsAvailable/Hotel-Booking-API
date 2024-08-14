from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import reqparse, fields, Resource, marshal_with

from hotel_booking.apis.schemas import room_fields
from hotel_booking.models.models import RoomType, Room
from hotel_booking.services.modifying_services import add_data
from hotel_booking.utils.utils import check_hotel_manager, generate_id

post_parser = reqparse.RequestParser()
post_parser.add_argument('no', type=int, location='json', required=True)
post_parser.add_argument('price', type=int, location='json', required=True)
post_parser.add_argument('type', location='json', required=True)
post_parser.add_argument('description', location='json', required=True)
post_parser.add_argument('capacity', type=int, location='json', required=True)

room_list_fields = {
    fields.List(fields.Nested(room_fields))
}


class RoomApi(Resource):
    @marshal_with(room_fields)
    @jwt_required()
    def post(self, hotel_id):
        manager_id = get_jwt_identity()
        if check_hotel_manager(hotel_id, manager_id):
            args = post_parser.parse_args()
            room_id = generate_id()
            room_type_id = generate_id()
            room_type = RoomType(room_type_id, args.type, args.description)
            room = Room(room_id, args.no, args.price, room_type_id, args.capacity, hotel_id)
            add_data(room_type)
            add_data(room)
            return room, room_type
        return {'msg': ''}, 403
