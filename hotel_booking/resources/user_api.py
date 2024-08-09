from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import reqparse, fields, Resource, marshal_with

from hotel_booking.models.models import User
from hotel_booking.services.hotel_manager_services import get_hotel_managers
from hotel_booking.services.modifying_services import add_data, update_data, delete_data
from hotel_booking.services.user_services import get_user_by_email, get_user, list_users
from hotel_booking.utils.utils import generate_id, hash_password, authorize, update_user, generate_verification_token

post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', location='json', required=True)
post_parser.add_argument('last_name', location='json', required=True)
post_parser.add_argument('email', location='json', required=True)
post_parser.add_argument('password', location='json', required=True)
post_parser.add_argument('role', location='json')

user_fields = {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'role': fields.String
}


class UserApi(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user_id = generate_id()
        token = generate_verification_token()
        hashed_password = hash_password(args.password)
        user = User(user_id, args.first_name, args.last_name, args.email, hashed_password, args.role, token)
        add_data(user)
        return user

    @marshal_with(user_fields)
    def get(self):
        args = post_parser.parse_args()
        user = get_user_by_email(args.email)
        if user is None:
            return {"msg": "Username or password is invalid."}, 401
        is_valid = authorize(args.password, user.password)
        if is_valid:
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return {"msg": "Username or password is invalid."}, 401

    @marshal_with(user_fields)
    @jwt_required()
    def put(self):
        args = post_parser.parse_args()
        user_id = get_jwt_identity()
        user = get_user(user_id)
        if user is None:
            return {'msg': 'Invalid id.'}, 404
        user = update_user(user, args)
        update_data(user)
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = get_user(user_id)
        if user.role is 'manager':
            hotel_managers = get_hotel_managers(user.id)
            for hotel_manager in hotel_managers:
                delete_data(hotel_manager)
        delete_data(user)
        return 200


class DeleteUserByAdmin(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def delete(self, user_id):
        claims = get_jwt()
        if (claims['role'] == 'admin'):
            user = get_user(user_id)
            if user is None:
                return {'msg': 'Invalid id.'}, 404
            if user.role is 'manager':
                hotel_managers = get_hotel_managers(user.id)
                for hotel_manager in hotel_managers:
                    delete_data(hotel_manager)
            delete_data(user)
            return 200
        return {'msg': 'This operation is restricted to admin.'}, 403


class ListUser(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if (claims['role'] == 'admin'):
            users = list_users()
            return users
        return {'msg': 'This operation is restricted to admin.'}, 403
