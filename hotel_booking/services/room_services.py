from hotel_booking.models.models import Room, RoomImage


def list_rooms(hotel_id):
    return Room.query.filter(Room.hotel_id == hotel_id).all()


def get_room(id):
    return Room.query.filter(Room.id == id).one_or_none()


def get_room_image(room_id):
    return RoomImage.query.filter(RoomImage.room_id == room_id).all()
