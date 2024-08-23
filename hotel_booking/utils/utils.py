import datetime
import random
import secrets
import string

from hotel_booking.app import bcrypt


def generate_id(length=20):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length))
    return id


def generate_verification_token(length=32):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


def convert_string_to_date(date_string):
    date_object = datetime.datetime.fromisoformat(date_string)
    return date_object.date()


def subtract_2_date(date1, date2):
    delta = date2 - date1
    return delta.days


def hash_password(raw_password):
    hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
    return hashed_password


def authorize(requested_password, password):
    is_valid = bcrypt.check_password_hash(password, requested_password)
    return is_valid
