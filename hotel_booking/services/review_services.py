from hotel_booking.models.models import ReviewImage, Review
from hotel_booking.services.modifying_services import add_data, update_data
from hotel_booking.utils.utils import generate_id


def get_reviews_by_room_id(room_id):
    return Review.query.filter(Review.room_id == room_id).all()


def get_review_by_user_id_and_review_id(user_id, review_id):
    return Review.query.filter(Review.user_id == user_id, Review.id == id).one_or_none()


def get_review_image_by_path(image_path):
    return ReviewImage.query.filter(ReviewImage.image_path == image_path).one_or_none()


def get_review_images_by_review_id(review_id):
    return ReviewImage.query.filter(ReviewImage.review_id == review_id).all()


def update_review_images(review_id, image_paths):
    if image_paths:
        for image_path in image_paths:
            review_image = get_review_image_by_path(image_path)
            if review_image is None:
                review_image_id = generate_id()
                review_image = ReviewImage(review_image_id, image_path, review_id)
                add_data(review_image)


def update_review(review, args):
    if args.star is not None:
        review.star = args.star
    elif args.title is not None:
        review.title = args.title
    elif args.comment is not None:
        review.comment = args.comment
    update_data(review)
    return review
