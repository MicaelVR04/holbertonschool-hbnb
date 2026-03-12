from app.models.base_model import BaseModel, db


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Review -> Place (many-to-one)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)
    place = db.relationship("Place", back_populates="reviews")

    # Review -> User (many-to-one)
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")
