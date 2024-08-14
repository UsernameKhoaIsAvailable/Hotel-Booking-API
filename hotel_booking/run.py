from hotel_booking.app import app, db, api
from hotel_booking.apis.booking_api import BookingApi
from hotel_booking.apis.hotel_api import HotelApi, SearchHotel
from hotel_booking.apis.user_api import UserApi

api.add_resource(BookingApi, '/bookings')
api.add_resource(UserApi, '/user')
api.add_resource(HotelApi, '/hotels/<string:id>')
api.add_resource(SearchHotel, '/hotels')
db.init_app(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
