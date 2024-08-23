from hotel_booking.models.models import Room, RoomImage
from hotel_booking.services.modifying_services import add_data, update_data
from hotel_booking.utils.utils import generate_id


def list_rooms(hotel_id):
    return Room.query.filter(Room.hotel_id == hotel_id).all()


def get_room(id):
    return Room.query.filter(Room.id == id).one_or_none()


def get_room_image_by_path(image_path):
    return RoomImage.query.filter(RoomImage.image_path == image_path).one_or_none()


def get_room_images_by_room_id(room_id):
    return RoomImage.query.filter(RoomImage.room_id == room_id).all()


def get_room_image(id):
    return RoomImage.query.filter(RoomImage.id == id).one_or_none()


def update_room_images(room_id, image_paths):
    if image_paths:
        for image_path in image_paths:
            room_image = get_room_image_by_path(image_path)
            if room_image is None:
                room_image_id = generate_id()
                room_image = RoomImage(room_image_id, image_path, room_id)
                add_data(room_image)


def update_room(room, args):
    if args.no is not None:
        room.no = args.no
    elif args.price is not None:
        room.price = args.price
    elif args.type_id is not None:
        room.type_id = args.type_id
    elif args.capacity is not None:
        room.capacity = args.capacity
    update_data(room)
    return room
