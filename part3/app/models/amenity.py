from app.models.base_model import BaseModel, db
from app.models.place import place_amenity


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)

    # Amenity <-> Place (many-to-many)
    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
        lazy="subquery",
    )
