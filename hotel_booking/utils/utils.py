import secrets
import string
import random

from hotel_booking.app import bcrypt


def generate_id(length=20):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length))
    return id


def generate_verification_token(length=32):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def hash_password(raw_password):
    hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
    return hashed_password


def authorize(requested_password, password):
    is_valid = bcrypt.check_password_hash(password, requested_password)
    return is_valid


def update_hotel(hotel, args):
    hotel.name = args.name
    hotel.address = args.address
    hotel.district = args.district
    hotel.city = args.city
    hotel.classification = args.classification
    hotel.description = args.description
    return hotel


def update_user(user, args):
    user.first_name = args.first_name
    user.last_name = args.last_name
    user.email = args.email
    hashed_password = hash_password(args.password)
    user.password = hashed_password
    return user
