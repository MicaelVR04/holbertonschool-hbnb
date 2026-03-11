from app.models.base_model import BaseModel, db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)
