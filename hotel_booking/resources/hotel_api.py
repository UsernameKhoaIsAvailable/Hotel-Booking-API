from flask_restful import Resource, fields, reqparse, marshal_with
from hotel_booking.models.models import Hotel
from hotel_booking.services.modifying_services import add_data
from hotel_booking.utils.utils import generate_id

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
    def post(self):
        args = post_parser.parse_args()
        id = generate_id()
        hotel = Hotel(id, args.name, args.address, args.district, args.city, args.classification, args.description)
        add_data(hotel)
        return hotel
