from hotel_booking.models.models import Hotel, Booking, Room, HotelImage


def search_hotel(district, city, checkin, checkout, capacity):
    return Hotel.query.join(Booking, (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
            (Booking.expected_check_in < checkin) & (Booking.expected_check_out > checkout))).filter(
        Hotel.city == city).all()
    # return Hotel.query.join(Booking, (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
    #         (Booking.expected_check_in < checkin) &
    #         (Booking.expected_check_out > checkout))).join(Room,
    #                                                        Room.capacity == capacity).filter(
    #     Hotel.city == city, Hotel.district == district).order_by(Room.price & Hotel.classification).all()


def search_hotel_by_district(district, city, checkin, checkout):
    return Hotel.query.join(Booking, (Booking.expected_check_out < checkin) | (Booking.expected_check_in > checkout) | (
            (Booking.expected_check_in < checkin) & (Booking.expected_check_out > checkout))).filter(
        Hotel.district == district, Hotel.city == city).all()



def get_hotel(id):
    return Hotel.query.filter(Hotel.id == id).one_or_none()


def get_hotel_images(hotel_id):
    return HotelImage.query.filter(HotelImage.hotel_id == hotel_id).all()
