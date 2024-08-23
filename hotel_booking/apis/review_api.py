from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, marshal_with, reqparse

from hotel_booking.apis.schemas import review_fields, review_list_fields
from hotel_booking.models.models import Review
from hotel_booking.services.modifying_services import add_data, delete_data
from hotel_booking.services.review_services import update_review_images, get_review_images_by_review_id, \
    get_reviews_by_room_id, get_review_by_user_id_and_review_id, update_review
from hotel_booking.utils.utils import generate_id


class AddAndGetListReview(Resource):
    @marshal_with(review_fields)
    @jwt_required()
    def post(self, room_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('star', location='json', required=True)
        post_parser.add_argument('title', location='json', required=True)
        post_parser.add_argument('comment', location='json', required=True)
        post_parser.add_argument('image_paths', location='json', action='append')
        args = post_parser.parse_args()
        user_id = get_jwt_identity()
        review_id = generate_id()
        review = Review(review_id, args.star, args.title, args.comment, user_id, room_id)
        add_data(review)
        update_review_images(review_id, args.image_paths)
        images = get_review_images_by_review_id(review_id)
        review.images = images
        return review

    @marshal_with(review_list_fields)
    def get(self, room_id):
        reviews = get_reviews_by_room_id(room_id)
        for review in reviews:
            images = get_review_images_by_review_id(review.id)
            review.images = images
        return reviews


class UpdateAndDeleteReview(Resource):
    @marshal_with(review_fields)
    @jwt_required()
    def put(self, review_id):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('star', location='json')
        post_parser.add_argument('title', location='json')
        post_parser.add_argument('comment', location='json')
        post_parser.add_argument('image_paths', location='json', action='append')
        user_id = get_jwt_identity()
        review = get_review_by_user_id_and_review_id(user_id, review_id)
        if review is not None:
            args = post_parser.parse_args()
            review = update_review(review, args)
            update_review_images(review_id, args.image_paths)
            images = get_review_images_by_review_id(review_id)
            review.images = images
            return review
        return {'msg': 'This comment does not belong to current user.'}, 403

    @jwt_required()
    def delete(self, review_id):
        user_id = get_jwt_identity()
        review = get_review_by_user_id_and_review_id(user_id, review_id)
        if review is not None:
            delete_data(review)
            return 200
        return {'msg': 'This comment does not belong to current user.'}, 403
