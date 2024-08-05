import string
import random

from hotel_booking.app import bcrypt


def generate_id(length=20):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length))
    return id


def hash_password(raw_password):
    hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
    return hashed_password


def authorize(requested_password, password):
    is_valid = bcrypt.check_password_hash(password, requested_password)
    return is_valid
