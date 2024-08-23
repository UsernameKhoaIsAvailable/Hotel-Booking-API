from hotel_booking.models.models import Voucher
from hotel_booking.services.modifying_services import update_data


def get_vouchers_by_hotel_id(hotel_id):
    return Voucher.query.filter(Voucher.hotel_id == hotel_id).all()


def get_voucher(id):
    return Voucher.query.filter(Voucher.id == id).one_or_none()


def update_voucher(voucher, args):
    if args.name is not None:
        voucher.name = args.name
    if args.discount is not None:
        voucher.discount = args.discount
    update_data(voucher)
    return voucher
