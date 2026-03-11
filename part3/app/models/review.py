from app.models.base_model import BaseModel, db


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(60), nullable=False)
