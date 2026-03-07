from app.models.base_model import BaseModel, db

class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    places = db.relationship("Place", backref="owner", lazy=True)
    reviews = db.relationship("Review", backref="author", lazy=True)
