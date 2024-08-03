from hotel_booking.resources.room import Room
from hotel_booking.resources.room_image import RoomImage


def search_room(hotel_id):
    return Room.query.filter(Room.hotel_id == hotel_id).all()


def search_a_room(id):
    return Room.query.filter(Room.id == id).one_or_none()


def search_room_image(room_id):
    return RoomImage.query.filter(RoomImage.room_id == room_id).all()
