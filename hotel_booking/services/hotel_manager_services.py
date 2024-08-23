from hotel_booking.models.models import HotelManager, Room, HotelImage, RoomImage


def get_hotel_manager(hotel_id, manager_id):
    return HotelManager.query.filter(HotelManager.hotel_id == hotel_id,
                                     HotelManager.manager_id == manager_id).one_or_none()


def get_hotel_manager_by_room_id(room_id, manager_id):
    return HotelManager.query.join(Room).filter(Room.id == room_id, HotelManager.manager_id == manager_id).one_or_none()


def get_hotel_manager_by_room_image_id(room_image_id, manager_id):
    return HotelManager.query.join(Room).join(RoomImage).filter(RoomImage.id == room_image_id,
                                                                HotelManager.manager_id == manager_id).one_or_none()


def check_hotel_manager(hotel_id, manager_id):
    hotel_manager = get_hotel_manager(hotel_id, manager_id)
    if hotel_manager is None:
        return False
    return True


def check_hotel_manager_by_room_id(room_id, manager_id):
    hotel_manager = get_hotel_manager_by_room_id(room_id, manager_id)
    if hotel_manager is None:
        return False
    return True


def check_hotel_manager_by_room_image_id(room_image_id, manager_id):
    hotel_manager = get_hotel_manager_by_room_image_id(room_image_id, manager_id)
    if hotel_manager is None:
        return False
    return True
