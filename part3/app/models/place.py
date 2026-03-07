from app.models.base_model import BaseModel, db

class Place(BaseModel):
    """Place model."""

    __tablename__ = "places"

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)

    reviews = db.relationship("Review", backref="place", lazy=True)
