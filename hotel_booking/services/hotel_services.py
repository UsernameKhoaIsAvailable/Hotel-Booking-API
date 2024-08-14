from sqlalchemy import select, func, or_, and_

from hotel_booking.app import db
from hotel_booking.models.models import Hotel, Booking, Room, HotelImage
from hotel_booking.services.modifying_services import update_data


def search_hotel(city, checkin, checkout, capacity=None, district=None):
    query = select(Hotel, db.session.query(func.min(Room.price)).group_by(Room.hotel_id).subquery(),
                   HotelImage.image_path).join(Room).join(HotelImage).join(Booking).where(Hotel.city == city,
                                                                                          or_(Booking.expected_check_out < checkin,
                                                                                              Booking.expected_check_in > checkout,
                                                                                              and_(
                                                                                                  Booking.expected_check_in < checkin,
                                                                                                  Booking.expected_check_out > checkout)))
    if district is not None:
        query.where(Hotel.district == district)
    elif capacity is not None:
        query.where(Room.capacity == capacity)
    return db.session.execute(query).all()

    # query = Hotel.query.join(Booking,
    #                          (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
    #                                  (Booking.expected_check_in < checkin) & (
    #                                      Booking.expected_check_out > checkout))).filter(
    #     Hotel.city == city)
    # if district is not None:

    # return Hotel.query.join(Booking, (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
    #         (Booking.expected_check_in < checkin) &
    #         (Booking.expected_check_out > checkout))).join(Room,
    #                                                        Room.capacity == capacity).filter(
    #     Hotel.city == city, Hotel.district == district).order_by(Room.price & Hotel.classification).all()

    # def search_hotel_by_district(district, city, checkin, checkout):
    #     return Hotel.query.join(Booking, (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
    #             (Booking.expected_check_in < checkin) & (Booking.expected_check_out > checkout))).filter(
    #         Hotel.district == district, Hotel.city == city).all()


def get_hotel(id):
    return Hotel.query.filter(Hotel.id == id).one_or_none()


def get_hotel_images(hotel_id):
    return HotelImage.query.filter(HotelImage.hotel_id == hotel_id).all()


def update_hotel(hotel, args):
    hotel.name = args.name
    hotel.address = args.address
    hotel.district = args.district
    hotel.city = args.city
    hotel.classification = args.classification
    if args.description is not None:
        hotel.description = args.description
    update_data(hotel)
    return hotel
