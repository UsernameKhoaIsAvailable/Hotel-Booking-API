from hotel_booking.models.models import RoomType
from hotel_booking.services.modifying_services import update_data


def get_room_type(id):
    return RoomType.query.filter(RoomType.id == id).one_or_none()


def get_room_types_by_hotel_id(hotel_id):
    return RoomType.query.filter(RoomType.hotel_id == hotel_id).all()


def update_room_type(room_type, args):
    if args.name is not None:
        room_type.name = args.name
    elif args.description is not None:
        room_type.description = args.description
    update_data(room_type)
    return room_type
