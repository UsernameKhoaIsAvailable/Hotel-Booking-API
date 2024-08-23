from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource, marshal_with

from hotel_booking.apis.schemas import service_fields, service_list_fields
from hotel_booking.models.models import Services
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.services import get_services_by_hotel_id, get_service, update_service
from hotel_booking.utils.utils import generate_id
from hotel_booking.services.hotel_manager_services import check_hotel_manager


class AddAndGetListService(Resource):
    @marshal_with(service_fields)
    @jwt_required()
    def post(self, hotel_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json', required=True)
        post_parser.add_argument('description', location='json', required=True)
        post_parser.add_argument('price', type=int, location='json', required=True)
        manager_id = get_jwt_identity()
        if check_hotel_manager(hotel_id, manager_id):
            args = post_parser.parse_args()
            service_id = generate_id()
            service = Services(service_id, args.name, args.description, args.price, hotel_id)
            add_data(service)
            return service
        return {'msg': 'This operation is restricted to managers.'}, 403

    @marshal_with(service_list_fields)
    def get(self, hotel_id):
        services = get_services_by_hotel_id(hotel_id)
        return services


class UpdateAndDeleteService(Resource):
    @marshal_with(service_fields)
    @jwt_required()
    def put(self, service_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', location='json')
        post_parser.add_argument('description', location='json')
        post_parser.add_argument('price', type=int, location='json')
        service = get_service(service_id)
        manager_id = get_jwt_identity()
        if check_hotel_manager(service.hotel_id, manager_id):
            args = post_parser.parse_args()
            service = update_service(service, args)
            return service
        return {'msg': 'This operation is restricted to managers.'}, 403

    @jwt_required()
    def delete(self, service_id):
        service = get_service(service_id)
        manager_id = get_jwt_identity()
        if check_hotel_manager(service.hotel_id, manager_id):
            delete_data(service)
            return 200
        return {'msg': 'This operation is restricted to managers.'}, 403
