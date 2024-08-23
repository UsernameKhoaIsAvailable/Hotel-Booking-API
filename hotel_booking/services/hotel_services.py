from sqlalchemy import select, func, or_, and_

from hotel_booking.app import db
from hotel_booking.models.models import Hotel, Booking, Room, HotelImage
from hotel_booking.services.modifying_services import update_data, add_data
from hotel_booking.utils.utils import generate_id


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


def get_hotel_image(id):
    return HotelImage.query.filter(HotelImage.id == id).one_or_none()


def get_hotel_image_by_path(image_path):
    return HotelImage.query.filter(HotelImage.image_path == image_path).one_or_none()


def get_hotel_images_by_hotel_id(hotel_id):
    return HotelImage.query.filter(HotelImage.hotel_id == hotel_id).all()


def update_hotel(hotel, args):
    if args.name is not None:
        hotel.name = args.name
    elif args.name is not None:
        hotel.address = args.address
    elif args.name is not None:
        hotel.district = args.district
    elif args.name is not None:
        hotel.city = args.city
    elif args.name is not None:
        hotel.classification = args.classification
    elif args.description is not None:
        hotel.description = args.description
    update_data(hotel)
    return hotel


def update_hotel_images(hotel_id, image_paths):
    if image_paths:
        for image_path in image_paths:
            hotel_image = get_hotel_image_by_path(image_path)
            if hotel_image is None:
                hotel_image_id = generate_id()
                hotel_image = HotelImage(hotel_image_id, image_path, hotel_id)
                add_data(hotel_image)
