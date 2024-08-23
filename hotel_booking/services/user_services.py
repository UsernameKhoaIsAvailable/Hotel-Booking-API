from hotel_booking.models.models import User
from hotel_booking.services.modifying_services import update_data
from hotel_booking.utils.utils import hash_password


def get_user_by_email(email):
    return User.query.filter(User.email == email).one_or_none()


def get_user(id):
    return User.query.filter(User.id == id).one_or_none()


def list_users():
    return User.query.all()


def update_user(user, args):
    if args.first_name is not None:
        user.first_name = args.first_name
    if args.last_name is not None:
        user.last_name = args.last_name
    if args.email is not None:
        user.email = args.email
    if args.password is not None:
        hashed_password = hash_password(args.password)
        user.password = hashed_password
    if args.role is not None:
        user.role = args.role
    update_data(user)
    return user
