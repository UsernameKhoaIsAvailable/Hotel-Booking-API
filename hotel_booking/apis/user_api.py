from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import reqparse, Resource, marshal_with
from sqlalchemy import True_

from hotel_booking.apis.schemas import user_fields, user_list_fields
from hotel_booking.models.models import User
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.user_services import get_user_by_email, get_user, list_users, update_user
from hotel_booking.utils.utils import generate_id, hash_password, authorize, generate_verification_token


class UserApi(Resource):
    @marshal_with(user_fields)
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('first_name', location='json', required=True)
        post_parser.add_argument('last_name', location='json', required=True)
        post_parser.add_argument('email', location='json', required=True)
        post_parser.add_argument('password', location='json', required=True)
        post_parser.add_argument('role', location='json', required=True)
        args = post_parser.parse_args()
        user_id = generate_id()
        token = generate_verification_token()
        hashed_password = hash_password(args.password)
        user = User(user_id, args.first_name, args.last_name, args.email, hashed_password, args.role, token)
        add_data(user)
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('first_name', location='json')
        post_parser.add_argument('last_name', location='json')
        post_parser.add_argument('email', location='json')
        post_parser.add_argument('password', location='json')
        post_parser.add_argument('role', location='json')
        args = post_parser.parse_args()
        user_id = get_jwt_identity()
        user = get_user(user_id)
        user = update_user(user, args)
        return user

    @marshal_with(user_fields)
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = get_user(user_id)
        delete_data(user)
        return 200

    @marshal_with(user_list_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] == 'admin':
            users = list_users()
            return users
        return {'msg': 'This operation is restricted to admin.'}, 403


class Login(Resource):
    def post(self, email):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('password', location='json', required=True)
        args = post_parser.parse_args()
        user = get_user_by_email(email)
        if user is None:
            return {"msg": "Username or password is invalid."}, 401
        is_valid = authorize(args.password, user.password)
        if is_valid:
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return {"msg": "Username or password is invalid."}, 401


class DeleteUserByAdmin(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def delete(self, user_id):
        claims = get_jwt()
        if claims['role'] == 'admin':
            user = get_user(user_id)
            if user is None:
                return {'msg': 'User not found.'}, 404
            delete_data(user)
            return 200
        return {'msg': 'This operation is restricted to admin.'}, 403


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        claims = get_jwt()
        access_token = create_access_token(identity=identity, additional_claims=claims)
        return jsonify(access_token=access_token)
