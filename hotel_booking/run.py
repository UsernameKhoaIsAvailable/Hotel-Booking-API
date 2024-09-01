from hotel_booking.apis.booking_api import AddBooking, GetAndUpdateBooking, ConfirmBooking, GetUserBookingList, \
    GetHotelBookingList
from hotel_booking.apis.hotel_api import HotelApi, AddAndSearchHotel, DeleteHotelImage
from hotel_booking.apis.room_api import AddRoom, RoomApi, GetRoomList, DeleteRoomImage
from hotel_booking.apis.room_type_api import AddAndGetListRoomType, UpdateAndDeleteRoomType
from hotel_booking.apis.services_api import AddAndGetListService, UpdateAndDeleteService
from hotel_booking.apis.user_api import UserApi, Login, DeleteUserByAdmin, RefreshToken
from hotel_booking.apis.voucher_api import AddAndGetListVoucher, UpdateAndDeleteVoucher
from hotel_booking.app import app, db, api

api.add_resource(Login, '/users/<string:email>')
api.add_resource(RefreshToken, '/refresh')
api.add_resource(UserApi, '/users')
api.add_resource(GetUserBookingList, '/users/bookings')
api.add_resource(DeleteUserByAdmin, '/users/<string:user_id>')
api.add_resource(AddAndSearchHotel, '/hotels')
api.add_resource(HotelApi, '/hotels/<string:hotel_id>')
api.add_resource(DeleteHotelImage, '/hotels/images/<string:image_id>')
api.add_resource(AddAndGetListRoomType, '/hotels/<string:hotel_id>/roomTypes')
api.add_resource(UpdateAndDeleteRoomType, '/hotels/roomTypes/<string:room_type_id>')
api.add_resource(AddRoom, '/hotels/<string:hotel_id>/rooms')
api.add_resource(RoomApi, '/hotels/rooms/<string:room_id>')
api.add_resource(GetRoomList, '/hotels/rooms')
api.add_resource(DeleteRoomImage, '/hotels/rooms/images/<string:image_id>')
api.add_resource(AddAndGetListService, '/hotels/<string:hotel_id>/services')
api.add_resource(UpdateAndDeleteService, '/hotels/services/<string:service_id>')
api.add_resource(AddAndGetListVoucher, '/hotels/<string:hotel_id>/vouchers')
api.add_resource(UpdateAndDeleteVoucher, '/hotels/vouchers/<string:voucher_id>')
api.add_resource(GetHotelBookingList, '/hotels/<string:hotel_id>/bookings')
api.add_resource(AddBooking, '/bookings')
api.add_resource(GetAndUpdateBooking, '/bookings/<string:booking_id>')
api.add_resource(ConfirmBooking, '/bookings/<string:booking_id>/confirm')


db.init_app(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
