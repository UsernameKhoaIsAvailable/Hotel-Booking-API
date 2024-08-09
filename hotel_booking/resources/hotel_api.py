from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, fields, reqparse, marshal_with
from hotel_booking.models.models import Hotel, HotelManager
from hotel_booking.services.hotel_manager_services import get_hotel_managers_by_hotel_id
from hotel_booking.services.hotel_services import get_hotel
from hotel_booking.services.modifying_services import add_data, update_data, delete_data
from hotel_booking.utils.utils import generate_id, update_hotel

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', location='json', required=True)
post_parser.add_argument('address', location='json', required=True)
post_parser.add_argument('district', location='json', required=True)
post_parser.add_argument('city', location='json', required=True)
post_parser.add_argument('classification', type=int, location='json', required=True)
post_parser.add_argument('description', location='json')

hotel_fields = {
    'id': fields.String,
    'name': fields.String,
    'address': fields.String,
    'district': fields.String,
    'city': fields.String,
    'classification': fields.Integer,
    'description': fields.String,
}

hotel_list_fields = {
    fields.List(fields.Nested(hotel_fields))
}


class HotelApi(Resource):
    @marshal_with(hotel_fields)
    @jwt_required()
    def put(self, hotel_id):
        claims = get_jwt()
        if (claims['role'] == 'manager'):
            args = post_parser.parse_args()
            hotel = get_hotel(hotel_id)
            if hotel is None:
                return {'msg': 'Invalid id.'}, 404
            hotel = update_hotel(hotel, args)
            update_data(hotel)
            return hotel
        return {'msg': 'This operation is restricted to managers.'}, 403

    @marshal_with(hotel_fields)
    @jwt_required()
    def delete(self, hotel_id):
        claims = get_jwt()
        if (claims['role'] == 'manager'):
            hotel = get_hotel(hotel_id)
            if hotel is None:
                return {'msg': 'Invalid id.'}, 404
            hotel_managers = get_hotel_managers_by_hotel_id(hotel_id)
            for hotel_manager in hotel_managers:
                delete_data(hotel_manager)
            delete_data(hotel)
            return 200
        return {'msg': 'This operation is restricted to managers.'}, 403

    @marshal_with(hotel_fields)
    def get(self, hotel_id):
        hotel = get_hotel(hotel_id)
        if hotel is None:
            return {'msg': 'Invalid id.'}, 404
        return hotel


class AddHotel(Resource):
    @marshal_with(hotel_fields)
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if (claims['role'] == 'manager'):
            args = post_parser.parse_args()
            hotel_id = generate_id()
            hotel = Hotel(hotel_id, args.name, args.address, args.district, args.city, args.classification,
                          args.description)
            add_data(hotel)
            hotel_manager_id = generate_id()
            manager_id = get_jwt_identity()
            hotel_manager = HotelManager(hotel_manager_id, manager_id, hotel_id)
            add_data(hotel_manager)
            return hotel
        return {'msg': 'This operation is restricted to managers.'}, 403


class SearchHotel(Resource):
    @marshal_with(hotel_fields)
    def get(self):
        args = request.args
