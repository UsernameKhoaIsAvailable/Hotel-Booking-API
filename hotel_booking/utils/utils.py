import datetime
import secrets
import string
import random

from hotel_booking.app import bcrypt
from hotel_booking.models.models import ChosenServices, ChosenVoucher
from hotel_booking.services.booking_services import search_chosen_service, get_service, search_chosen_voucher, \
    get_voucher
from hotel_booking.services.hotel_manager_services import get_hotel_manager, get_hotel_manager_by_room_id
from hotel_booking.services.modifying_services import add_data


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


def calculate_base_price(service_ids, booking_id, base_price):
    if service_ids:
        for service_id in service_ids:
            chosen_service = search_chosen_service(service_id, booking_id)
            if chosen_service is None:
                chosen_service_id = generate_id()
                chosen_service = ChosenServices(chosen_service_id, service_id, booking_id)
                add_data(chosen_service)
            service = get_service(service_id)
            base_price += service.price
    return base_price


def calculate_total_price(voucher_ids, booking_id, base_price):
    discount = 0
    total_price = 0
    if voucher_ids:
        for voucher_id in voucher_ids:
            chosen_voucher = search_chosen_voucher(voucher_id, booking_id)
            if chosen_voucher is None:
                chosen_voucher_id = generate_id()
                chosen_voucher = ChosenVoucher(chosen_voucher_id, voucher_id, booking_id)
                add_data(chosen_voucher)
            voucher = get_voucher(voucher_id)
            discount += voucher.discount
    total_price -= base_price * discount / 100
    return total_price


def check_hotel_manager(hotel_id, manager_id):
    hotel_manager = get_hotel_manager(hotel_id, manager_id)
    if hotel_manager is None:
        return False
    return True


def check_hotel_manager_by_room_id(room_id, manager_id):
    hotel_manager = get_hotel_manager_by_room_id(room_id, manager_id)
    if hotel_manager is None:
        return False
    return True
