from hotel_booking.models.models import Booking, ChosenVoucher, ChosenServices, Services, Room


def get_booking(id):
    return Booking.query.join(ChosenServices).join(ChosenVoucher).filter(Booking.id == id).one_or_none()


def get_list_chosen_services(booking_id):
    return Services.query.join(ChosenServices, ChosenServices.booking_id == booking_id).all()


def list_bookings(hotel_id):
    return Booking.query.join(Room, Room.hotel_id == hotel_id).all()


def get_service(id):
    return Services.query.filter(Services.id == id).one_or_none()
