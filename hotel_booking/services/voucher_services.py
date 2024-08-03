from hotel_booking.resources.voucher import Voucher


def search_voucher(hotel_id):
    return Voucher.query.filter(Voucher.hotel_id == hotel_id).all()


def search_a_voucher(id):
    return Voucher.query.filter(Voucher.id == id).one_or_none()
