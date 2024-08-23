from hotel_booking.models.models import Services
from hotel_booking.services.modifying_services import update_data


def get_service(id):
    return Services.query.filter(Services.id == id).one_or_none()


def get_services_by_hotel_id(hotel_id):
    return Services.query.filter(Services.hotel_id == hotel_id).all()


def update_service(service, args):
    if args.name is not None:
        service.name = args.name
    if args.description is not None:
        service.description = args.description
    if args.price is not None:
        service.price = args.price
    update_data(service)
    return service
