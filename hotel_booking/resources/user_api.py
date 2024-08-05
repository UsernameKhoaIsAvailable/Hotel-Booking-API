from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import reqparse, fields, Resource, marshal_with

from hotel_booking.models.models import User
from hotel_booking.services.modifying_services import add_data
from hotel_booking.services.user_services import get_user
from hotel_booking.utils.utils import generate_id, hash_password, authorize

post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', location='json')
post_parser.add_argument('last_name', location='json')
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


class UserRegisterApi(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user_id = generate_id()
        hashed_password = hash_password(args.password)
        user = User(user_id, args.first_name, args.last_name, args.email, hashed_password, args.role)
        add_data(user)
        return user


class UserLoginApi(Resource):
    def get(self):
        args = post_parser.parse_args()
        user = get_user(args.email)
        if user is None:
            return jsonify({"msg": "Username or password is invalid"})
        is_valid = authorize(args.password, user.password)
        if is_valid:
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return jsonify({"msg": "Username or password is invalid"})
