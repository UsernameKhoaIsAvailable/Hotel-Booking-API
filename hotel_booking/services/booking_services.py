from hotel_booking.models.models import Booking, ChosenVoucher, ChosenServices, Services, Room, Voucher
from hotel_booking.services.modifying_services import update_data, add_data
from hotel_booking.services.room_services import get_room
from hotel_booking.services.services import get_service
from hotel_booking.services.voucher_services import get_voucher
from hotel_booking.utils.utils import convert_string_to_date, subtract_2_date, generate_id


def get_booking(id):
    return Booking.query.join(ChosenServices).join(ChosenVoucher).filter(Booking.id == id).one_or_none()


def get_bookings_by_user_id(user_id):
    return Booking.query.filter(Booking.user_id == user_id).all()


def get_bookings_by_hotel_id(hotel_id):
    return Booking.query.join(Room).filter(Room.hotel_id == hotel_id).all()


def get_chosen_services_by_booking_id(booking_id):
    return Services.query.join(ChosenServices, ChosenServices.booking_id == booking_id).all()


def get_chosen_service(service_id, booking_id):
    return ChosenServices.query.filter(ChosenServices.service_id == service_id,
                                       ChosenServices.booking_id == booking_id).one_or_none()


def get_chosen_vouchers_by_booking_id(booking_id):
    return Voucher.query.join(ChosenVoucher).filter(ChosenVoucher.booking_id == booking_id).all()


def get_chosen_voucher(voucher_id, booking_id):
    return ChosenVoucher.query.filter(ChosenVoucher.voucher_id == voucher_id,
                                      ChosenVoucher.booking_id == booking_id).one_or_none()


def update_booking(booking, args):
    if args.expected_check_in is not None:
        booking.expected_check_in = convert_string_to_date(args.expected_check_in)
    elif args.expected_check_in is not None:
        booking.expected_check_out = convert_string_to_date(args.expected_check_out)
    days = subtract_2_date(booking.expected_check_in, booking.expected_check_out)
    if args.room_id is not None:
        booking.room_id = args.room_id
    base_price = get_room(booking.room_id).price * days
    base_price = calculate_base_price(args.service_ids, booking.id, base_price)
    total_price = calculate_total_price(args.voucher_ids, booking.id, base_price)
    booking.base_price = base_price
    booking.total_price = total_price
    update_data(booking)
    return booking


def get_booking_list(bookings):
    i = 0
    while i < len(bookings):
        bookings[i] = return_booking(bookings[i])
    return {'bookings': bookings}


def calculate_base_price(service_ids, booking_id, base_price):
    if service_ids:
        for service_id in service_ids:
            chosen_service = get_chosen_service(service_id, booking_id)
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
            chosen_voucher = get_chosen_voucher(voucher_id, booking_id)
            if chosen_voucher is None:
                chosen_voucher_id = generate_id()
                chosen_voucher = ChosenVoucher(chosen_voucher_id, voucher_id, booking_id)
                add_data(chosen_voucher)
            voucher = get_voucher(voucher_id)
            discount += voucher.discount
    total_price -= base_price * discount / 100
    return total_price


def return_booking(booking, room=None):
    if room is None:
        room = get_room(booking.room_id)
    chosen_services = get_chosen_services_by_booking_id(booking.id)
    chosen_vouchers = get_chosen_vouchers_by_booking_id(booking.id)
    booking.room = room
    booking.services = chosen_services
    booking.vouchers = chosen_vouchers
    return booking
