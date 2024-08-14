from hotel_booking.app import db


class ReviewImage(db.Model):
    id = db.Column(db.CHAR(50), primary_key=True)
    image_path = db.Column(db.String, nullable=False)
    user_id = db.Column(db.CHAR(50), db.ForeignKey('User.id'))

    # user = db.relationship('User', backref='review_images')
