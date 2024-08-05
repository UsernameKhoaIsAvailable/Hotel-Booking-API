from hotel_booking.models.models import Voucher


def list_vouchers(hotel_id):
    return Voucher.query.filter(Voucher.hotel_id == hotel_id).all()


def get_voucher(id):
    return Voucher.query.filter(Voucher.id == id).one_or_none()
