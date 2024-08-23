from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource, marshal_with

from hotel_booking.apis.schemas import room_fields
from hotel_booking.models.models import Room
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.room_services import update_room_images, get_room_images_by_room_id, get_room, \
    update_room, get_room_image
from hotel_booking.services.room_type_services import get_room_type
from hotel_booking.utils.utils import generate_id
from hotel_booking.services.hotel_manager_services import check_hotel_manager, check_hotel_manager_by_room_image_id


class AddRoom(Resource):
    @marshal_with(room_fields)
    @jwt_required()
    def post(self, hotel_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('no', type=int, location='json', required=True)
        post_parser.add_argument('price', type=int, location='json', required=True)
        post_parser.add_argument('type_id', location='json', required=True)
        post_parser.add_argument('capacity', type=int, location='json', required=True)
        post_parser.add_argument('image_paths', location='json', action='append')
        manager_id = get_jwt_identity()
        if check_hotel_manager(hotel_id, manager_id):
            args = post_parser.parse_args()
            room_type = get_room_type(args.type_id)
            if room_type is None:
                return {'msg': 'Room type not found.'}, 404
            room_id = generate_id()
            room = Room(room_id, args.no, args.price, args.type_id, args.capacity, hotel_id)
            add_data(room)
            update_room_images(room_id, args.image_paths)
            images = get_room_images_by_room_id(room_id)
            return room, room_type, images
        return {'msg': ''}, 403


class RoomApi(Resource):
    @marshal_with(room_fields)
    def get(self, room_id):
        room = get_room(room_id)
        if room is None:
            return {'msg': 'Room not found.'}, 404
        room_type = get_room_type(room.type_id)
        images = get_room_images_by_room_id(room_id)
        return room, room_type, images

    @marshal_with(room_fields)
    @jwt_required()
    def put(self, room_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('no', type=int, location='json')
        post_parser.add_argument('price', type=int, location='json')
        post_parser.add_argument('type_id', location='json')
        post_parser.add_argument('capacity', type=int, location='json')
        post_parser.add_argument('image_paths', location='json', action='append')
        args = post_parser.parse_args()
        manager_id = get_jwt_identity()
        room = get_room(room_id)
        if room is None:
            return {'msg': 'Room not found'}, 404
        elif check_hotel_manager(room.hotel_id, manager_id):
            room = update_room(room, args)
            update_room_images(room_id, args.image_paths)
            images = get_room_images_by_room_id(room_id)
            room_type = get_room_type(room.type_id)
            return room, room_type, images
        return {'msg': ''}, 403

    @jwt_required()
    def delete(self, room_id):
        manager_id = get_jwt_identity()
        room = get_room(room_id)
        if room is None:
            return {'msg': 'Room not found'}, 404
        if check_hotel_manager(room.hotel_id, manager_id):
            delete_data(room)
            return 200
        return {'msg': ''}, 403


class GetRoomList(Resource):
    def get(self, hotel_id):
        return


class DeleteRoomImage(Resource):
    @jwt_required()
    def delete(self, image_id):
        manager_id = get_jwt_identity()
        if check_hotel_manager_by_room_image_id(image_id, manager_id):
            image = get_room_image(image_id)
            delete_data(image)
            return 200
        return {'msg': ''}, 403
