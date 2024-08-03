from hotel_booking.models.models import Booking
from hotel_booking.resources.chosen_services import ChosenServices
from hotel_booking.resources.room import Room
from hotel_booking.resources.services import Services


def search_a_booking(id):
    return Booking.query.filter(Booking.id == id).one_or_none()


def search_chosen_services(booking_id):
    return Services.query.join(ChosenServices, ChosenServices.booking_id == booking_id).all()


def search_booking(hotel_id):
    return Booking.query.join(Room, Room.hotel_id == hotel_id).all()


def search_a_service(id):
    return Services.query.filter(Services.id == id).one_or_none()
