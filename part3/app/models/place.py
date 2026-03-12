from app.models.base_model import BaseModel, db

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(60), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(60), db.ForeignKey("amenities.id"), primary_key=True),
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # User -> Place (one-to-many)
    owner_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="places")

    # Place -> Review (one-to-many)
    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan", lazy=True)

    # Place <-> Amenity (many-to-many)
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy="subquery",
    )
