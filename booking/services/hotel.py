from operator import or_, and_

from booking.app import db
from booking.resources.models import Hotel, Booking, Room


def add_hotel(hotel):
    db.session.add(hotel)
    db.session.commit()


def update_hotel(hotel):
    hotel.verified = True
    db.session.commit()


def delete_hotel(hotel):
    db.session.delete(hotel)
    db.session.commit()


def search_hotel(district, city, checkin, checkout, capacity):
    Hotel.query.join(Booking.room_id).join(Room).filter(Hotel.city == city, Hotel.district == district,
                                                        or_(Booking.expected_check_out < checkin,
                                                            Booking.expected_check_in > checkout,
                                                            and_(Booking.expected_check_in < checkin,
                                                                 Booking.expected_check_out > checkout)),
                                                        Room.id == Booking.room_id, Room.hotel_id == Hotel.id,
                                                        Room.capacity == capacity)


def search_a_hotel(id):
    Hotel.query.filter(Hotel.id == id).one_or_none()
