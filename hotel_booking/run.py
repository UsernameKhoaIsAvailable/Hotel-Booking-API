from hotel_booking.app import app, db, api
from hotel_booking.resources.booking_api import BookingApi
from hotel_booking.resources.user_api import UserRegisterApi, UserLoginApi

api.add_resource(BookingApi, '/bookings')
api.add_resource(UserRegisterApi, '/users/register')
api.add_resource(UserLoginApi, '/users/login')
db.init_app(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
