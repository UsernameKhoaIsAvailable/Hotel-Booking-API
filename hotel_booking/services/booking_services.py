from hotel_booking.models.models import Booking, ChosenVoucher, ChosenServices, Services, Room, Voucher
from hotel_booking.services.modifying_services import update_data
from hotel_booking.services.room_services import get_room
from hotel_booking.utils.utils import convert_string_to_date, subtract_2_date, calculate_base_price, \
    calculate_total_price


def get_booking(id):
    return Booking.query.join(ChosenServices).join(ChosenVoucher).filter(Booking.id == id).one_or_none()


def search_chosen_services(booking_id):
    return Services.query.join(ChosenServices, ChosenServices.booking_id == booking_id).all()


def list_bookings(hotel_id):
    return Booking.query.join(Room, Room.hotel_id == hotel_id).all()


def get_service(id):
    return Services.query.filter(Services.id == id).one_or_none()


def search_chosen_service(service_id, booking_id):
    return ChosenServices.query.filter(ChosenServices.service_id == service_id,
                                       ChosenServices.booking_id == booking_id).one_or_none()


def list_vouchers(hotel_id):
    return Voucher.query.filter(Voucher.hotel_id == hotel_id).all()


def get_voucher(id):
    return Voucher.query.filter(Voucher.id == id).one_or_none()


def search_chosen_vouchers(booking_id):
    return Voucher.query.join(ChosenVoucher).filter(ChosenVoucher.booking_id == booking_id).all()


def search_chosen_voucher(voucher_id, booking_id):
    return ChosenVoucher.query.filter(ChosenVoucher.voucher_id == voucher_id,
                                      ChosenVoucher.booking_id == booking_id).one_or_none()


def update_booking(booking, args):
    expected_check_in = convert_string_to_date(args.expected_check_in)
    expected_check_out = convert_string_to_date(args.expected_check_out)
    if subtract_2_date(booking.expected_check_out, booking.expected_check_out) != subtract_2_date(expected_check_in,
                                                                                                  expected_check_out):
        booking.expected_check_in = expected_check_in
        booking.expected_check_out = expected_check_out
    days = subtract_2_date(booking.expected_check_in, booking.expected_check_out)
    if args.room_id != booking.room_id:
        booking.room_id = args.room_id
    base_price = get_room(booking.room_id).price * days
    base_price = calculate_base_price(args.service_ids, booking.id, base_price)
    total_price = calculate_total_price(args.voucher_ids, booking.id, base_price)
    booking.base_price = base_price
    booking.total_price = total_price
    update_data(booking)
    return booking
