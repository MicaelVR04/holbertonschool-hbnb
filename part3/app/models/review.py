from app.models.base_model import BaseModel, db

class Review(BaseModel):
    """Review model."""

    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)
