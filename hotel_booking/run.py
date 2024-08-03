from hotel_booking.app import app, db, api
from hotel_booking.resources.hotel_api import HotelApi

api.add_resource(HotelApi, '/hotel')
db.init_app(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
